/* EmergSmart · Service Worker · cache-first offline */
var CACHE = 'emergsmart-v1';
var ASSETS = [
  '/emergsmart/',
  '/emergsmart/index.html',
  '/emergsmart/manifest.json',
  '/emergsmart/icon-192.png',
  '/emergsmart/icon-512.png'
];

self.addEventListener('install', function (e) {
  e.waitUntil(
    caches.open(CACHE).then(function (c) {
      return c.addAll(ASSETS);
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener('activate', function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k !== CACHE) { return caches.delete(k); }
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener('fetch', function (e) {
  if (e.request.method !== 'GET') { return; }
  // cache-first: si hay cache lo devuelve; si no, va a red y guarda copia
  e.respondWith(
    caches.match(e.request).then(function (cached) {
      if (cached) { return cached; }
      return fetch(e.request).then(function (resp) {
        var copy = resp.clone();
        caches.open(CACHE).then(function (c) {
          try { c.put(e.request, copy); } catch (err) {}
        });
        return resp;
      }).catch(function () {
        // offline y sin cache: fallback a la app
        return caches.match('/emergsmart/index.html');
      });
    })
  );
});
