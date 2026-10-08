// Service Worker for Unitree Go PWA
const CACHE_NAME = 'unitreego-v1';

self.addEventListener('install', (event) => {
    self.skipWaiting();
});

self.addEventListener('activate', (event) => {
    event.waitUntil(clients.claim());
});

self.addEventListener('fetch', (event) => {
    // Luôn ưu tiên mạng cho WebSocket và API điều khiển robot
    if (event.request.url.includes('/api/') || event.request.url.includes('/ws')) {
        return;
    }
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});
