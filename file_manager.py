#!/usr/bin/env python3
"""
File Upload and Management System for Garage Management System
Handles file uploads, storage, and retrieval
"""
import os
import base64
import mimetypes
from pathlib import Path
from datetime import datetime
import json
import hashlib

# Configuration
UPLOAD_DIR = Path(__file__).parent / 'uploads'
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {
    'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'],
    'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls'],
    'all': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls']
}

# Initialize upload directories
def init_upload_dirs():
    """Create upload directories if they don't exist"""
    dirs = ['jobs', 'invoices', 'customers', 'general']
    for dir_name in dirs:
        (UPLOAD_DIR / dir_name).mkdir(parents=True, exist_ok=True)
    print(f"[FILES] Upload directories initialized at {UPLOAD_DIR}")

def get_file_hash(file_data):
    """Generate hash for file data"""
    return hashlib.md5(file_data).hexdigest()

def is_allowed_file(filename, file_type='all'):
    """Check if file extension is allowed"""
    ext = Path(filename).suffix.lower()
    return ext in ALLOWED_EXTENSIONS.get(file_type, ALLOWED_EXTENSIONS['all'])

def save_file(file_data, filename, category='general', related_id=None):
    """
    Save uploaded file
    
    Args:
        file_data: Binary file data or base64 encoded string
        filename: Original filename
        category: Category (jobs, invoices, customers, general)
        related_id: ID of related entity (job_id, invoice_id, etc.)
    
    Returns:
        dict: File information including path and URL
    """
    # Validate file size
    if isinstance(file_data, str):
        # Base64 encoded
        file_data = base64.b64decode(file_data)
    
    if len(file_data) > MAX_FILE_SIZE:
        raise ValueError(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / 1024 / 1024}MB")
    
    # Validate file type
    if not is_allowed_file(filename):
        raise ValueError(f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS['all'])}")
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_hash = get_file_hash(file_data)[:8]
    ext = Path(filename).suffix
    safe_filename = f"{timestamp}_{file_hash}_{Path(filename).stem[:50]}{ext}"
    
    # Determine save path
    category_dir = UPLOAD_DIR / category
    if related_id:
        category_dir = category_dir / str(related_id)
    category_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = category_dir / safe_filename
    
    # Save file
    with open(filepath, 'wb') as f:
        f.write(file_data)
    
    # Get file info
    file_info = {
        'filename': safe_filename,
        'original_filename': filename,
        'filepath': str(filepath),
        'category': category,
        'related_id': related_id,
        'size': len(file_data),
        'mime_type': mimetypes.guess_type(filename)[0],
        'uploaded_at': datetime.now().isoformat(),
        'url': f"/uploads/{category}/{related_id}/{safe_filename}" if related_id else f"/uploads/{category}/{safe_filename}"
    }
    
    # Save metadata
    save_file_metadata(file_info)
    
    print(f"[FILES] File saved: {safe_filename} ({len(file_data)} bytes)")
    return file_info

def save_file_metadata(file_info):
    """Save file metadata to JSON"""
    metadata_file = UPLOAD_DIR / 'metadata.json'
    
    # Load existing metadata
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
    else:
        metadata = []
    
    # Add new file info
    metadata.append(file_info)
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)

def get_files_by_category(category, related_id=None):
    """Get all files for a category"""
    metadata_file = UPLOAD_DIR / 'metadata.json'
    
    if not metadata_file.exists():
        return []
    
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Filter by category and related_id
    files = [f for f in metadata if f['category'] == category]
    if related_id:
        files = [f for f in files if f.get('related_id') == related_id]
    
    return files

def delete_file(filepath):
    """Delete a file and its metadata"""
    filepath = Path(filepath)
    
    if filepath.exists():
        filepath.unlink()
        print(f"[FILES] File deleted: {filepath.name}")
        
        # Remove from metadata
        metadata_file = UPLOAD_DIR / 'metadata.json'
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            metadata = [f for f in metadata if f['filepath'] != str(filepath)]
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        
        return True
    return False

def get_file_info(filepath):
    """Get file information"""
    filepath = Path(filepath)
    
    if not filepath.exists():
        return None
    
    metadata_file = UPLOAD_DIR / 'metadata.json'
    if metadata_file.exists():
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
        
        for file_info in metadata:
            if file_info['filepath'] == str(filepath):
                return file_info
    
    # Return basic info if not in metadata
    return {
        'filename': filepath.name,
        'filepath': str(filepath),
        'size': filepath.stat().st_size,
        'mime_type': mimetypes.guess_type(str(filepath))[0]
    }

def get_storage_stats():
    """Get storage statistics"""
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(UPLOAD_DIR):
        for file in files:
            if file != 'metadata.json':
                filepath = Path(root) / file
                total_size += filepath.stat().st_size
                file_count += 1
    
    return {
        'total_files': file_count,
        'total_size_bytes': total_size,
        'total_size_mb': round(total_size / 1024 / 1024, 2),
        'upload_dir': str(UPLOAD_DIR)
    }

# Initialize on import
init_upload_dirs()

if __name__ == "__main__":
    print("File Manager Module")
    print(f"Upload directory: {UPLOAD_DIR}")
    print(f"Allowed extensions: {ALLOWED_EXTENSIONS['all']}")
