/**
 * Service Worker for Garage Management System PWA
 * Provides offline functionality and caching
 */

const CACHE_NAME = 'gms-v1.3.0';
const OFFLINE_URL = '/offline.html';

// Files to cache on install
const CACHE_FILES = [
    '/',
    '/index.html',
    '/garage-dashboard.html',
    '/invoices.html',
    '/customers.html',
    '/vat-reports.html',
    '/settings.html',
    '/mobile-responsive.css',
    '/mobile-nav.js',
    '/mobile-table-cards.js',
    '/js/api.js',
    '/js/dashboard.js',
    '/js/translations.js',
    '/js/settings-manager.js',
    '/professional_modal_styles.css',
    '/professional_notifications.js',
    OFFLINE_URL
];

// Install event - cache files
self.addEventListener('install', event => {
    console.log('[Service Worker] Installing...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('[Service Worker] Caching app shell');
                return cache.addAll(CACHE_FILES);
            })
            .then(() => {
                console.log('[Service Worker] Skip waiting');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('[Service Worker] Cache failed:', error);
            })
    );
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
    console.log('[Service Worker] Activating...');
    
    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(cacheName => cacheName !== CACHE_NAME)
                        .map(cacheName => {
                            console.log('[Service Worker] Deleting old cache:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
            .then(() => {
                console.log('[Service Worker] Claiming clients');
                return self.clients.claim();
            })
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', event => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') return;
    
    // Skip chrome-extension and other schemes
    if (!event.request.url.startsWith('http')) return;
    
    // NEVER cache API requests - always go to network
    if (event.request.url.includes('/api/')) {
        event.respondWith(fetch(event.request));
        return;
    }

    event.respondWith(
        caches.match(event.request)
            .then(cachedResponse => {
                // Return cached version if available
                if (cachedResponse) {
                    console.log('[Service Worker] Serving from cache:', event.request.url);
                    return cachedResponse;
                }

                // Fetch from network
                return fetch(event.request)
                    .then(response => {
                        // Don't cache if not a success
                        if (!response || response.status !== 200 || response.type !== 'basic') {
                            return response;
                        }

                        // Clone the response
                        const responseToCache = response.clone();

                        // Cache the new response
                        caches.open(CACHE_NAME)
                            .then(cache => {
                                // Only cache GET requests for specific types
                                if (event.request.url.match(/\.(html|css|js|png|jpg|jpeg|svg|json)$/)) {
                                    cache.put(event.request, responseToCache);
                                }
                            });

                        return response;
                    })
                    .catch(error => {
                        console.log('[Service Worker] Fetch failed, serving offline page:', error);
                        
                        // Serve offline page for navigation requests
                        if (event.request.mode === 'navigate') {
                            return caches.match(OFFLINE_URL);
                        }
                        
                        return new Response('Offline - Please check your internet connection', {
                            status: 503,
                            statusText: 'Service Unavailable',
                            headers: new Headers({
                                'Content-Type': 'text/plain'
                            })
                        });
                    });
            })
    );
});

// Message event - handle messages from clients
self.addEventListener('message', event => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data && event.data.type === 'CLEAR_CACHE') {
        event.waitUntil(
            caches.keys().then(cacheNames => {
                return Promise.all(
                    cacheNames.map(cacheName => caches.delete(cacheName))
                );
            })
        );
    }
});

// Push notification event
self.addEventListener('push', event => {
    const options = {
        body: event.data ? event.data.text() : 'New notification from GMS',
        icon: '/icons/icon-192x192.png',
        badge: '/icons/icon-72x72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View',
                icon: '/icons/icon-96x96.png'
            },
            {
                action: 'close',
                title: 'Close',
                icon: '/icons/icon-96x96.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('Garage Management System', options)
    );
});

// Notification click event
self.addEventListener('notificationclick', event => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

console.log('[Service Worker] Loaded');
