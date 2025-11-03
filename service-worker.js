/**
 * Service Worker for Garage Management System PWA
 * COMPLETELY DISABLED - Prevents all caching and offline issues
 * VERSION: 2025-11-03-10-05 - FORCE UPDATE
 */

// Install event - Force immediate activation
self.addEventListener('install', event => {
    console.log('[Service Worker] FORCE UPDATE v2025-11-03-10-05 - Clearing all cache');
    self.skipWaiting();
});

// Activate event - Delete ALL old caches
self.addEventListener('activate', event => {
    console.log('[Service Worker] Activating - Deleting ALL old caches');
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cacheName => {
                    console.log('[Service Worker] Deleting cache:', cacheName);
                    return caches.delete(cacheName);
                })
            );
        }).then(() => {
            console.log('[Service Worker] All caches cleared - Ready for fresh content');
            return self.clients.claim();
        })
    );
});

// Fetch event - Pass all requests to network (NO CACHING)
self.addEventListener('fetch', event => {
    console.log('[Service Worker] DISABLED - All requests go to network:', event.request.url);
    
    // Do NOT intercept any requests - let them go to network
    // This prevents offline.html from being served for API calls
    event.respondWith(fetch(event.request));
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
