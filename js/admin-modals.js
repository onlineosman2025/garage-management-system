// Professional Modal Functions for Admin Dashboard

// Edit User Modal
function editUser(garageId, userId) {
    const user = allUsers.find(u => u.id === userId && u.garage_id === garageId);
    if (!user) {
        showToast('❌ User not found!', 'error');
        return;
    }

    // Populate form
    document.getElementById('editUserGarageId').value = garageId;
    document.getElementById('editUserId').value = userId;
    document.getElementById('editUserName').value = user.name;
    document.getElementById('editUserEmail').value = user.email;
    document.getElementById('editUserRole').value = user.role;
    document.getElementById('editUserPhone').value = user.phone || '';
    
    openModal('editUserModal');
}

async function submitEditUser() {
    const form = document.getElementById('editUserForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const garageId = document.getElementById('editUserGarageId').value;
    const userId = document.getElementById('editUserId').value;
    const name = document.getElementById('editUserName').value;
    const email = document.getElementById('editUserEmail').value;
    const role = document.getElementById('editUserRole').value;
    const phone = document.getElementById('editUserPhone').value;

    try {
        const response = await fetch(`${api.baseURL}/admin/users/${garageId}/${userId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({ name, email, role, phone })
        });

        if (response.ok) {
            showToast('✅ User updated successfully!', 'success');
            closeModal('editUserModal');
            await refreshDashboard();
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error updating user:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}

// Edit Garage Modal
async function editGarage(garageId) {
    const garage = allGarages.find(g => g.garage_id === garageId);
    if (!garage) {
        showToast('❌ Garage not found!', 'error');
        return;
    }

    // Populate form
    document.getElementById('editGarageId').value = garageId;
    document.getElementById('editGarageName').value = garage.garage_name;
    document.getElementById('editGarageOwner').value = garage.owner_name;
    document.getElementById('editGarageEmail').value = garage.email;
    document.getElementById('editGaragePhone').value = garage.phone || '';
    
    openModal('editGarageModal');
}

async function submitEditGarage() {
    const form = document.getElementById('editGarageForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const garageId = document.getElementById('editGarageId').value;
    const garage_name = document.getElementById('editGarageName').value;
    const owner_name = document.getElementById('editGarageOwner').value;
    const email = document.getElementById('editGarageEmail').value;
    const phone = document.getElementById('editGaragePhone').value;

    try {
        const response = await fetch(`${api.baseURL}/admin/garages/${garageId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({ garage_name, owner_name, email, phone })
        });

        if (response.ok) {
            showToast('✅ Garage updated successfully!', 'success');
            closeModal('editGarageModal');
            await refreshDashboard();
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error updating garage:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}

// Reset Password Modal
async function resetPassword(garageId, userId, userName) {
    document.getElementById('resetPasswordGarageId').value = garageId;
    document.getElementById('resetPasswordUserId').value = userId;
    document.getElementById('resetPasswordUserName').textContent = userName;
    document.getElementById('resetPasswordForm').reset();
    
    openModal('resetPasswordModal');
}

async function submitResetPassword() {
    const form = document.getElementById('resetPasswordForm');
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const garageId = document.getElementById('resetPasswordGarageId').value;
    const userId = document.getElementById('resetPasswordUserId').value;
    const newPassword = document.getElementById('resetPasswordNew').value;
    const confirmPassword = document.getElementById('resetPasswordConfirm').value;

    if (newPassword !== confirmPassword) {
        showToast('❌ Passwords do not match!', 'error');
        return;
    }

    try {
        const response = await fetch(`${api.baseURL}/admin/users/${garageId}/${userId}/reset-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({ password: newPassword })
        });

        if (response.ok) {
            showToast('✅ Password reset successfully!', 'success');
            closeModal('resetPasswordModal');
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error resetting password:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}

// Suspend/Activate with confirmation
async function suspendGarage(garageId, garageName) {
    const reason = prompt(`Suspend "${garageName}"?\n\nEnter reason for suspension:`);
    if (!reason) return;

    try {
        const response = await fetch(`${api.baseURL}/admin/garages/${garageId}/suspend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({ reason })
        });

        if (response.ok) {
            showToast(`✅ Garage "${garageName}" suspended successfully!`, 'success');
            await refreshDashboard();
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error suspending garage:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}

async function activateGarage(garageId, garageName) {
    if (!confirm(`Activate "${garageName}"?`)) return;

    try {
        const response = await fetch(`${api.baseURL}/admin/garages/${garageId}/activate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            }
        });

        if (response.ok) {
            showToast(`✅ Garage "${garageName}" activated successfully!`, 'success');
            await refreshDashboard();
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error activating garage:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}

async function extendTrial(garageId, garageName) {
    const days = prompt(`Extend trial for "${garageName}"?\n\nEnter number of days to add:`, '14');
    if (!days || isNaN(days)) return;

    try {
        const response = await fetch(`${api.baseURL}/admin/garages/${garageId}/extend-trial`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('auth_token')}`
            },
            body: JSON.stringify({ days: parseInt(days) })
        });

        if (response.ok) {
            showToast(`✅ Trial extended by ${days} days for "${garageName}"!`, 'success');
            await refreshDashboard();
        } else {
            const error = await response.json();
            showToast(`❌ Failed: ${error.error || 'Unknown error'}`, 'error');
        }
    } catch (error) {
        console.error('Error extending trial:', error);
        showToast(`❌ Error: ${error.message}`, 'error');
    }
}
