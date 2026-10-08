// Service Worker for LEHOANG ROBOTICS PWA
const CACHE_NAME = 'lehoang-robotics-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Không can thiệp API và WebSocket
    if (event.request.url.includes('/api/') || event.request.url.includes('/ws')) {
        return;
    }
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
