// modules are defined as an array
// [ module function, map of requires ]
//
// map of requires is short require name -> numeric require
//
// anything defined in a previous bundle is accessed via the
// orig method which is the require for previous bundles

(function (modules, entry, mainEntry, parcelRequireName, globalName) {
  /* eslint-disable no-undef */
  var globalObject =
    typeof globalThis !== 'undefined'
      ? globalThis
      : typeof self !== 'undefined'
      ? self
      : typeof window !== 'undefined'
      ? window
      : typeof global !== 'undefined'
      ? global
      : {};
  /* eslint-enable no-undef */

  // Save the require from previous bundle to this closure if any
  var previousRequire =
    typeof globalObject[parcelRequireName] === 'function' &&
    globalObject[parcelRequireName];

  var cache = previousRequire.cache || {};
  // Do not use `require` to prevent Webpack from trying to bundle this call
  var nodeRequire =
    typeof module !== 'undefined' &&
    typeof module.require === 'function' &&
    module.require.bind(module);

  function newRequire(name, jumped) {
    if (!cache[name]) {
      if (!modules[name]) {
        // if we cannot find the module within our internal map or
        // cache jump to the current global require ie. the last bundle
        // that was added to the page.
        var currentRequire =
          typeof globalObject[parcelRequireName] === 'function' &&
          globalObject[parcelRequireName];
        if (!jumped && currentRequire) {
          return currentRequire(name, true);
        }

        // If there are other bundles on this page the require from the
        // previous one is saved to 'previousRequire'. Repeat this as
        // many times as there are bundles until the module is found or
        // we exhaust the require chain.
        if (previousRequire) {
          return previousRequire(name, true);
        }

        // Try the node require function if it exists.
        if (nodeRequire && typeof name === 'string') {
          return nodeRequire(name);
        }

        var err = new Error("Cannot find module '" + name + "'");
        err.code = 'MODULE_NOT_FOUND';
        throw err;
      }

      localRequire.resolve = resolve;
      localRequire.cache = {};

      var module = (cache[name] = new newRequire.Module(name));

      modules[name][0].call(
        module.exports,
        localRequire,
        module,
        module.exports,
        this
      );
    }

    return cache[name].exports;

    function localRequire(x) {
      var res = localRequire.resolve(x);
      return res === false ? {} : newRequire(res);
    }

    function resolve(x) {
      var id = modules[name][1][x];
      return id != null ? id : x;
    }
  }

  function Module(moduleName) {
    this.id = moduleName;
    this.bundle = newRequire;
    this.exports = {};
  }

  newRequire.isParcelRequire = true;
  newRequire.Module = Module;
  newRequire.modules = modules;
  newRequire.cache = cache;
  newRequire.parent = previousRequire;
  newRequire.register = function (id, exports) {
    modules[id] = [
      function (require, module) {
        module.exports = exports;
      },
      {},
    ];
  };

  Object.defineProperty(newRequire, 'root', {
    get: function () {
      return globalObject[parcelRequireName];
    },
  });

  globalObject[parcelRequireName] = newRequire;

  for (var i = 0; i < entry.length; i++) {
    newRequire(entry[i]);
  }

  if (mainEntry) {
    // Expose entry point to Node, AMD or browser globals
    // Based on https://github.com/ForbesLindesay/umd/blob/master/template.js
    var mainExports = newRequire(mainEntry);

    // CommonJS
    if (typeof exports === 'object' && typeof module !== 'undefined') {
      module.exports = mainExports;

      // RequireJS
    } else if (typeof define === 'function' && define.amd) {
      define(function () {
        return mainExports;
      });

      // <script>
    } else if (globalName) {
      this[globalName] = mainExports;
    }
  }
})({"lNrhS":[function(require,module,exports) {
var global = arguments[3];
var HMR_HOST = null;
var HMR_PORT = 1234;
var HMR_SECURE = false;
var HMR_ENV_HASH = "d6ea1d42532a7575";
var HMR_USE_SSE = false;
module.bundle.HMR_BUNDLE_ID = "493ec81d1b39973f";
"use strict";
/* global HMR_HOST, HMR_PORT, HMR_ENV_HASH, HMR_SECURE, HMR_USE_SSE, chrome, browser, __parcel__import__, __parcel__importScripts__, ServiceWorkerGlobalScope */ /*::
import type {
  HMRAsset,
  HMRMessage,
} from '@parcel/reporter-dev-server/src/HMRServer.js';
interface ParcelRequire {
  (string): mixed;
  cache: {|[string]: ParcelModule|};
  hotData: {|[string]: mixed|};
  Module: any;
  parent: ?ParcelRequire;
  isParcelRequire: true;
  modules: {|[string]: [Function, {|[string]: string|}]|};
  HMR_BUNDLE_ID: string;
  root: ParcelRequire;
}
interface ParcelModule {
  hot: {|
    data: mixed,
    accept(cb: (Function) => void): void,
    dispose(cb: (mixed) => void): void,
    // accept(deps: Array<string> | string, cb: (Function) => void): void,
    // decline(): void,
    _acceptCallbacks: Array<(Function) => void>,
    _disposeCallbacks: Array<(mixed) => void>,
  |};
}
interface ExtensionContext {
  runtime: {|
    reload(): void,
    getURL(url: string): string;
    getManifest(): {manifest_version: number, ...};
  |};
}
declare var module: {bundle: ParcelRequire, ...};
declare var HMR_HOST: string;
declare var HMR_PORT: string;
declare var HMR_ENV_HASH: string;
declare var HMR_SECURE: boolean;
declare var HMR_USE_SSE: boolean;
declare var chrome: ExtensionContext;
declare var browser: ExtensionContext;
declare var __parcel__import__: (string) => Promise<void>;
declare var __parcel__importScripts__: (string) => Promise<void>;
declare var globalThis: typeof self;
declare var ServiceWorkerGlobalScope: Object;
*/ var OVERLAY_ID = "__parcel__error__overlay__";
var OldModule = module.bundle.Module;
function Module(moduleName) {
    OldModule.call(this, moduleName);
    this.hot = {
        data: module.bundle.hotData[moduleName],
        _acceptCallbacks: [],
        _disposeCallbacks: [],
        accept: function(fn) {
            this._acceptCallbacks.push(fn || function() {});
        },
        dispose: function(fn) {
            this._disposeCallbacks.push(fn);
        }
    };
    module.bundle.hotData[moduleName] = undefined;
}
module.bundle.Module = Module;
module.bundle.hotData = {};
var checkedAssets /*: {|[string]: boolean|} */ , assetsToDispose /*: Array<[ParcelRequire, string]> */ , assetsToAccept /*: Array<[ParcelRequire, string]> */ ;
function getHostname() {
    return HMR_HOST || (location.protocol.indexOf("http") === 0 ? location.hostname : "localhost");
}
function getPort() {
    return HMR_PORT || location.port;
}
// eslint-disable-next-line no-redeclare
var parent = module.bundle.parent;
if ((!parent || !parent.isParcelRequire) && typeof WebSocket !== "undefined") {
    var hostname = getHostname();
    var port = getPort();
    var protocol = HMR_SECURE || location.protocol == "https:" && ![
        "localhost",
        "127.0.0.1",
        "0.0.0.0"
    ].includes(hostname) ? "wss" : "ws";
    var ws;
    if (HMR_USE_SSE) ws = new EventSource("/__parcel_hmr");
    else try {
        ws = new WebSocket(protocol + "://" + hostname + (port ? ":" + port : "") + "/");
    } catch (err) {
        if (err.message) console.error(err.message);
        ws = {};
    }
    // Web extension context
    var extCtx = typeof browser === "undefined" ? typeof chrome === "undefined" ? null : chrome : browser;
    // Safari doesn't support sourceURL in error stacks.
    // eval may also be disabled via CSP, so do a quick check.
    var supportsSourceURL = false;
    try {
        (0, eval)('throw new Error("test"); //# sourceURL=test.js');
    } catch (err) {
        supportsSourceURL = err.stack.includes("test.js");
    }
    // $FlowFixMe
    ws.onmessage = async function(event /*: {data: string, ...} */ ) {
        checkedAssets = {} /*: {|[string]: boolean|} */ ;
        assetsToAccept = [];
        assetsToDispose = [];
        var data /*: HMRMessage */  = JSON.parse(event.data);
        if (data.type === "update") {
            // Remove error overlay if there is one
            if (typeof document !== "undefined") removeErrorOverlay();
            let assets = data.assets.filter((asset)=>asset.envHash === HMR_ENV_HASH);
            // Handle HMR Update
            let handled = assets.every((asset)=>{
                return asset.type === "css" || asset.type === "js" && hmrAcceptCheck(module.bundle.root, asset.id, asset.depsByBundle);
            });
            if (handled) {
                console.clear();
                // Dispatch custom event so other runtimes (e.g React Refresh) are aware.
                if (typeof window !== "undefined" && typeof CustomEvent !== "undefined") window.dispatchEvent(new CustomEvent("parcelhmraccept"));
                await hmrApplyUpdates(assets);
                // Dispose all old assets.
                let processedAssets = {} /*: {|[string]: boolean|} */ ;
                for(let i = 0; i < assetsToDispose.length; i++){
                    let id = assetsToDispose[i][1];
                    if (!processedAssets[id]) {
                        hmrDispose(assetsToDispose[i][0], id);
                        processedAssets[id] = true;
                    }
                }
                // Run accept callbacks. This will also re-execute other disposed assets in topological order.
                processedAssets = {};
                for(let i = 0; i < assetsToAccept.length; i++){
                    let id = assetsToAccept[i][1];
                    if (!processedAssets[id]) {
                        hmrAccept(assetsToAccept[i][0], id);
                        processedAssets[id] = true;
                    }
                }
            } else fullReload();
        }
        if (data.type === "error") {
            // Log parcel errors to console
            for (let ansiDiagnostic of data.diagnostics.ansi){
                let stack = ansiDiagnostic.codeframe ? ansiDiagnostic.codeframe : ansiDiagnostic.stack;
                console.error("\uD83D\uDEA8 [parcel]: " + ansiDiagnostic.message + "\n" + stack + "\n\n" + ansiDiagnostic.hints.join("\n"));
            }
            if (typeof document !== "undefined") {
                // Render the fancy html overlay
                removeErrorOverlay();
                var overlay = createErrorOverlay(data.diagnostics.html);
                // $FlowFixMe
                document.body.appendChild(overlay);
            }
        }
    };
    if (ws instanceof WebSocket) {
        ws.onerror = function(e) {
            if (e.message) console.error(e.message);
        };
        ws.onclose = function() {
            console.warn("[parcel] \uD83D\uDEA8 Connection to the HMR server was lost");
        };
    }
}
function removeErrorOverlay() {
    var overlay = document.getElementById(OVERLAY_ID);
    if (overlay) {
        overlay.remove();
        console.log("[parcel] \u2728 Error resolved");
    }
}
function createErrorOverlay(diagnostics) {
    var overlay = document.createElement("div");
    overlay.id = OVERLAY_ID;
    let errorHTML = '<div style="background: black; opacity: 0.85; font-size: 16px; color: white; position: fixed; height: 100%; width: 100%; top: 0px; left: 0px; padding: 30px; font-family: Menlo, Consolas, monospace; z-index: 9999;">';
    for (let diagnostic of diagnostics){
        let stack = diagnostic.frames.length ? diagnostic.frames.reduce((p, frame)=>{
            return `${p}
<a href="/__parcel_launch_editor?file=${encodeURIComponent(frame.location)}" style="text-decoration: underline; color: #888" onclick="fetch(this.href); return false">${frame.location}</a>
${frame.code}`;
        }, "") : diagnostic.stack;
        errorHTML += `
      <div>
        <div style="font-size: 18px; font-weight: bold; margin-top: 20px;">
          \u{1F6A8} ${diagnostic.message}
        </div>
        <pre>${stack}</pre>
        <div>
          ${diagnostic.hints.map((hint)=>"<div>\uD83D\uDCA1 " + hint + "</div>").join("")}
        </div>
        ${diagnostic.documentation ? `<div>\u{1F4DD} <a style="color: violet" href="${diagnostic.documentation}" target="_blank">Learn more</a></div>` : ""}
      </div>
    `;
    }
    errorHTML += "</div>";
    overlay.innerHTML = errorHTML;
    return overlay;
}
function fullReload() {
    if ("reload" in location) location.reload();
    else if (extCtx && extCtx.runtime && extCtx.runtime.reload) extCtx.runtime.reload();
}
function getParents(bundle, id) /*: Array<[ParcelRequire, string]> */ {
    var modules = bundle.modules;
    if (!modules) return [];
    var parents = [];
    var k, d, dep;
    for(k in modules)for(d in modules[k][1]){
        dep = modules[k][1][d];
        if (dep === id || Array.isArray(dep) && dep[dep.length - 1] === id) parents.push([
            bundle,
            k
        ]);
    }
    if (bundle.parent) parents = parents.concat(getParents(bundle.parent, id));
    return parents;
}
function updateLink(link) {
    var href = link.getAttribute("href");
    if (!href) return;
    var newLink = link.cloneNode();
    newLink.onload = function() {
        if (link.parentNode !== null) // $FlowFixMe
        link.parentNode.removeChild(link);
    };
    newLink.setAttribute("href", // $FlowFixMe
    href.split("?")[0] + "?" + Date.now());
    // $FlowFixMe
    link.parentNode.insertBefore(newLink, link.nextSibling);
}
var cssTimeout = null;
function reloadCSS() {
    if (cssTimeout) return;
    cssTimeout = setTimeout(function() {
        var links = document.querySelectorAll('link[rel="stylesheet"]');
        for(var i = 0; i < links.length; i++){
            // $FlowFixMe[incompatible-type]
            var href /*: string */  = links[i].getAttribute("href");
            var hostname = getHostname();
            var servedFromHMRServer = hostname === "localhost" ? new RegExp("^(https?:\\/\\/(0.0.0.0|127.0.0.1)|localhost):" + getPort()).test(href) : href.indexOf(hostname + ":" + getPort());
            var absolute = /^https?:\/\//i.test(href) && href.indexOf(location.origin) !== 0 && !servedFromHMRServer;
            if (!absolute) updateLink(links[i]);
        }
        cssTimeout = null;
    }, 50);
}
function hmrDownload(asset) {
    if (asset.type === "js") {
        if (typeof document !== "undefined") {
            let script = document.createElement("script");
            script.src = asset.url + "?t=" + Date.now();
            if (asset.outputFormat === "esmodule") script.type = "module";
            return new Promise((resolve, reject)=>{
                var _document$head;
                script.onload = ()=>resolve(script);
                script.onerror = reject;
                (_document$head = document.head) === null || _document$head === void 0 || _document$head.appendChild(script);
            });
        } else if (typeof importScripts === "function") {
            // Worker scripts
            if (asset.outputFormat === "esmodule") return import(asset.url + "?t=" + Date.now());
            else return new Promise((resolve, reject)=>{
                try {
                    importScripts(asset.url + "?t=" + Date.now());
                    resolve();
                } catch (err) {
                    reject(err);
                }
            });
        }
    }
}
async function hmrApplyUpdates(assets) {
    global.parcelHotUpdate = Object.create(null);
    let scriptsToRemove;
    try {
        // If sourceURL comments aren't supported in eval, we need to load
        // the update from the dev server over HTTP so that stack traces
        // are correct in errors/logs. This is much slower than eval, so
        // we only do it if needed (currently just Safari).
        // https://bugs.webkit.org/show_bug.cgi?id=137297
        // This path is also taken if a CSP disallows eval.
        if (!supportsSourceURL) {
            let promises = assets.map((asset)=>{
                var _hmrDownload;
                return (_hmrDownload = hmrDownload(asset)) === null || _hmrDownload === void 0 ? void 0 : _hmrDownload.catch((err)=>{
                    // Web extension fix
                    if (extCtx && extCtx.runtime && extCtx.runtime.getManifest().manifest_version == 3 && typeof ServiceWorkerGlobalScope != "undefined" && global instanceof ServiceWorkerGlobalScope) {
                        extCtx.runtime.reload();
                        return;
                    }
                    throw err;
                });
            });
            scriptsToRemove = await Promise.all(promises);
        }
        assets.forEach(function(asset) {
            hmrApply(module.bundle.root, asset);
        });
    } finally{
        delete global.parcelHotUpdate;
        if (scriptsToRemove) scriptsToRemove.forEach((script)=>{
            if (script) {
                var _document$head2;
                (_document$head2 = document.head) === null || _document$head2 === void 0 || _document$head2.removeChild(script);
            }
        });
    }
}
function hmrApply(bundle /*: ParcelRequire */ , asset /*:  HMRAsset */ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (asset.type === "css") reloadCSS();
    else if (asset.type === "js") {
        let deps = asset.depsByBundle[bundle.HMR_BUNDLE_ID];
        if (deps) {
            if (modules[asset.id]) {
                // Remove dependencies that are removed and will become orphaned.
                // This is necessary so that if the asset is added back again, the cache is gone, and we prevent a full page reload.
                let oldDeps = modules[asset.id][1];
                for(let dep in oldDeps)if (!deps[dep] || deps[dep] !== oldDeps[dep]) {
                    let id = oldDeps[dep];
                    let parents = getParents(module.bundle.root, id);
                    if (parents.length === 1) hmrDelete(module.bundle.root, id);
                }
            }
            if (supportsSourceURL) // Global eval. We would use `new Function` here but browser
            // support for source maps is better with eval.
            (0, eval)(asset.output);
            // $FlowFixMe
            let fn = global.parcelHotUpdate[asset.id];
            modules[asset.id] = [
                fn,
                deps
            ];
        } else if (bundle.parent) hmrApply(bundle.parent, asset);
    }
}
function hmrDelete(bundle, id) {
    let modules = bundle.modules;
    if (!modules) return;
    if (modules[id]) {
        // Collect dependencies that will become orphaned when this module is deleted.
        let deps = modules[id][1];
        let orphans = [];
        for(let dep in deps){
            let parents = getParents(module.bundle.root, deps[dep]);
            if (parents.length === 1) orphans.push(deps[dep]);
        }
        // Delete the module. This must be done before deleting dependencies in case of circular dependencies.
        delete modules[id];
        delete bundle.cache[id];
        // Now delete the orphans.
        orphans.forEach((id)=>{
            hmrDelete(module.bundle.root, id);
        });
    } else if (bundle.parent) hmrDelete(bundle.parent, id);
}
function hmrAcceptCheck(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    if (hmrAcceptCheckOne(bundle, id, depsByBundle)) return true;
    // Traverse parents breadth first. All possible ancestries must accept the HMR update, or we'll reload.
    let parents = getParents(module.bundle.root, id);
    let accepted = false;
    while(parents.length > 0){
        let v = parents.shift();
        let a = hmrAcceptCheckOne(v[0], v[1], null);
        if (a) // If this parent accepts, stop traversing upward, but still consider siblings.
        accepted = true;
        else {
            // Otherwise, queue the parents in the next level upward.
            let p = getParents(module.bundle.root, v[1]);
            if (p.length === 0) {
                // If there are no parents, then we've reached an entry without accepting. Reload.
                accepted = false;
                break;
            }
            parents.push(...p);
        }
    }
    return accepted;
}
function hmrAcceptCheckOne(bundle /*: ParcelRequire */ , id /*: string */ , depsByBundle /*: ?{ [string]: { [string]: string } }*/ ) {
    var modules = bundle.modules;
    if (!modules) return;
    if (depsByBundle && !depsByBundle[bundle.HMR_BUNDLE_ID]) {
        // If we reached the root bundle without finding where the asset should go,
        // there's nothing to do. Mark as "accepted" so we don't reload the page.
        if (!bundle.parent) return true;
        return hmrAcceptCheck(bundle.parent, id, depsByBundle);
    }
    if (checkedAssets[id]) return true;
    checkedAssets[id] = true;
    var cached = bundle.cache[id];
    assetsToDispose.push([
        bundle,
        id
    ]);
    if (!cached || cached.hot && cached.hot._acceptCallbacks.length) {
        assetsToAccept.push([
            bundle,
            id
        ]);
        return true;
    }
}
function hmrDispose(bundle /*: ParcelRequire */ , id /*: string */ ) {
    var cached = bundle.cache[id];
    bundle.hotData[id] = {};
    if (cached && cached.hot) cached.hot.data = bundle.hotData[id];
    if (cached && cached.hot && cached.hot._disposeCallbacks.length) cached.hot._disposeCallbacks.forEach(function(cb) {
        cb(bundle.hotData[id]);
    });
    delete bundle.cache[id];
}
function hmrAccept(bundle /*: ParcelRequire */ , id /*: string */ ) {
    // Execute the module.
    bundle(id);
    // Run the accept callbacks in the new version of the module.
    var cached = bundle.cache[id];
    if (cached && cached.hot && cached.hot._acceptCallbacks.length) cached.hot._acceptCallbacks.forEach(function(cb) {
        var assetsToAlsoAccept = cb(function() {
            return getParents(module.bundle.root, id);
        });
        if (assetsToAlsoAccept && assetsToAccept.length) {
            assetsToAlsoAccept.forEach(function(a) {
                hmrDispose(a[0], a[1]);
            });
            // $FlowFixMe[method-unbinding]
            assetsToAccept.push.apply(assetsToAccept, assetsToAlsoAccept);
        }
    });
}

},{}],"9RRD0":[function(require,module,exports) {
var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
var _autocompleteJs = require("bootstrap5-autocomplete/autocomplete.js");
var _autocompleteJsDefault = parcelHelpers.interopDefault(_autocompleteJs);
async function load() {
    navActivateCurrent();
    const userSearchInput = document.getElementById("userSearchInput");
    new (0, _autocompleteJsDefault.default)(userSearchInput, {
        "onSelectItem": userSelected
    });
}
function userSelected(item) {
    console.log("userSelected", item);
    const url = new URL(window.location.href);
    url.searchParams.delete("uid");
    url.searchParams.append("uid", item.value);
    window.location.href = url.href;
}
function navActivateCurrent() {
    for (let elem of document.getElementsByClassName("nav-link"))if (elem.tagName === "A") {
        if (elem.href.split("?")[0] === window.location.href.split("?")[0]) {
            elem.classList.add("active");
            elem.ariaCurrent = "page";
        } else {
            elem.classList.remove("active");
            elem.ariaCurrent = "";
        }
    }
}
window.addEventListener("load", load);

},{"bootstrap5-autocomplete/autocomplete.js":"hiuLP","@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"hiuLP":[function(require,module,exports) {
/**
 * Bootstrap 5 autocomplete
 */ // #region config
/**
 * @callback RenderCallback
 * @param {Object} item
 * @param {String} label
 * @param {Autocomplete} inst
 * @returns {string}
 */ /**
 * @callback ItemCallback
 * @param {Object} item
 * @param {Autocomplete} inst
 * @returns {void}
 */ /**
 * @callback ServerCallback
 * @param {Response} response
 * @param {Autocomplete} inst
 * @returns {Promise}
 */ /**
 * @callback ErrorCallback
 * @param {Error} e
 * @param {AbortSignal} signal
 * @param {Autocomplete} inst
 * @returns {void}
 */ /**
 * @callback FetchCallback
 * @param {Autocomplete} inst
 * @returns {void}
 */ /**
 * @typedef Config
 * @property {Boolean} showAllSuggestions Show all suggestions even if they don't match
 * @property {Number} suggestionsThreshold Number of chars required to show suggestions
 * @property {Number} maximumItems Maximum number of items to display
 * @property {Boolean} autoselectFirst Always select the first item
 * @property {Boolean} ignoreEnter Ignore enter if no items are selected (play nicely with autoselectFirst=0)
 * @property {Boolean} updateOnSelect Update input value on selection (doesn't play nice with autoselectFirst)
 * @property {Boolean} highlightTyped Highlight matched part of the label
 * @property {String} highlightClass Class added to the mark label
 * @property {Boolean} fullWidth Match the width on the input field
 * @property {Boolean} fixed Use fixed positioning (solve overflow issues)
 * @property {Boolean} fuzzy Fuzzy search
 * @property {Boolean} startsWith Must start with the string. Defaults to false (it matches any position).
 * @property {Boolean} fillIn Show fill in icon.
 * @property {Boolean} preventBrowserAutocomplete Additional measures to prevent browser autocomplete
 * @property {String} itemClass Applied to the dropdown item. Accepts space separated classes.
 * @property {Array} activeClasses By default: ["bg-primary", "text-white"]
 * @property {String} labelField Key for the label
 * @property {String} valueField Key for the value
 * @property {Array} searchFields Key for the search
 * @property {String} queryParam Key for the query parameter for server
 * @property {Array|Object} items An array of label/value objects or an object with key/values
 * @property {Function} source A function that provides the list of items
 * @property {Boolean} hiddenInput Create an hidden input which stores the valueField
 * @property {String} hiddenValue Populate the initial hidden value. Mostly useful with liveServer.
 * @property {String} clearControl Selector that will clear the input on click.
 * @property {String} datalist The id of the source datalist
 * @property {String} server Endpoint for data provider
 * @property {String} serverMethod HTTP request method for data provider, default is GET
 * @property {String|Object} serverParams Parameters to pass along to the server. You can specify a "related" key with the id of a related field.
 * @property {String} serverDataKey By default: data
 * @property {Object} fetchOptions Any other fetch options (https://developer.mozilla.org/en-US/docs/Web/API/fetch#syntax)
 * @property {Boolean} liveServer Should the endpoint be called each time on input
 * @property {Boolean} noCache Prevent caching by appending a timestamp
 * @property {Number} debounceTime Debounce time for live server
 * @property {String} notFoundMessage Display a no suggestions found message. Leave empty to disable
 * @property {RenderCallback} onRenderItem Callback function that returns the label
 * @property {ItemCallback} onSelectItem Callback function to call on selection
 * @property {ServerCallback} onServerResponse Callback function to process server response. Must return a Promise
 * @property {ErrorCallback} onServerError Callback function to process server errors.
 * @property {ItemCallback} onChange Callback function to call on change-event. Returns currently selected item if any
 * @property {FetchCallback} onBeforeFetch Callback function before fetch
 * @property {FetchCallback} onAfterFetch Callback function after fetch
 */ /**
 * @type {Config}
 */ var parcelHelpers = require("@parcel/transformer-js/src/esmodule-helpers.js");
parcelHelpers.defineInteropFlag(exports);
const DEFAULTS = {
    showAllSuggestions: false,
    suggestionsThreshold: 1,
    maximumItems: 0,
    autoselectFirst: true,
    ignoreEnter: false,
    updateOnSelect: false,
    highlightTyped: false,
    highlightClass: "",
    fullWidth: false,
    fixed: false,
    fuzzy: false,
    startsWith: false,
    fillIn: false,
    preventBrowserAutocomplete: false,
    itemClass: "",
    activeClasses: [
        "bg-primary",
        "text-white"
    ],
    labelField: "label",
    valueField: "value",
    searchFields: [
        "label"
    ],
    queryParam: "query",
    items: [],
    source: null,
    hiddenInput: false,
    hiddenValue: "",
    clearControl: "",
    datalist: "",
    server: "",
    serverMethod: "GET",
    serverParams: {},
    serverDataKey: "data",
    fetchOptions: {},
    liveServer: false,
    noCache: true,
    debounceTime: 300,
    notFoundMessage: "",
    onRenderItem: (item, label, inst)=>{
        return label;
    },
    onSelectItem: (item, inst)=>{},
    onServerResponse: (response, inst)=>{
        return response.json();
    },
    onServerError: (e, signal, inst)=>{
        // Current version of Firefox rejects the promise with a DOMException
        if (e.name === "AbortError" || signal.aborted) return;
        console.error(e);
    },
    onChange: (item, inst)=>{},
    onBeforeFetch: (inst)=>{},
    onAfterFetch: (inst)=>{}
};
// #endregion
// #region constants
const LOADING_CLASS = "is-loading";
const ACTIVE_CLASS = "is-active";
const SHOW_CLASS = "show";
const NEXT = "next";
const PREV = "prev";
const INSTANCE_MAP = new WeakMap();
let counter = 0;
let activeCounter = 0;
// #endregion
// #region functions
/**
 * @param {Function} func
 * @param {number} timeout
 * @returns {Function}
 */ function debounce(func, timeout = 300) {
    let timer;
    return (...args)=>{
        clearTimeout(timer);
        timer = setTimeout(()=>{
            //@ts-ignore
            func.apply(this, args);
        }, timeout);
    };
}
/**
 * @param {String} str
 * @returns {String}
 */ function removeDiacritics(str) {
    return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}
/**
 * @param {String|Number} str
 * @returns {String}
 */ function normalize(str) {
    if (!str) return "";
    return removeDiacritics(str.toString()).toLowerCase();
}
/**
 * A simple fuzzy match algorithm that checks if chars are matched
 * in order in the target string
 *
 * @param {String} str
 * @param {String} lookup
 * @returns {Boolean}
 */ function fuzzyMatch(str, lookup) {
    if (str.indexOf(lookup) >= 0) return true;
    let pos = 0;
    for(let i = 0; i < lookup.length; i++){
        const c = lookup[i];
        if (c == " ") continue;
        pos = str.indexOf(c, pos) + 1;
        if (pos <= 0) return false;
    }
    return true;
}
/**
 * @param {HTMLElement} el
 * @param {HTMLElement} newEl
 * @returns {HTMLElement}
 */ function insertAfter(el, newEl) {
    return el.parentNode.insertBefore(newEl, el.nextSibling);
}
/**
 * @param {string} html
 * @returns {string}
 */ function decodeHtml(html) {
    var txt = document.createElement("textarea");
    txt.innerHTML = html;
    return txt.value;
}
/**
 * @param {HTMLElement} el
 * @param {Object} attrs
 */ function attrs(el, attrs) {
    for (const [k, v] of Object.entries(attrs))el.setAttribute(k, v);
}
/**
 * Add a zero width join between chars
 * @param {HTMLElement|Element} el
 */ function zwijit(el) {
    //@ts-ignore
    el.ariaLabel = el.innerText;
    //@ts-ignore
    el.innerHTML = el.innerText.split("").map((char)=>char + "&zwj;").join("");
}
function nested(str, obj = "window") {
    return str.split(".").reduce((r, p)=>r[p], obj);
}
// #endregion
class Autocomplete {
    /**
   * @param {HTMLInputElement} el
   * @param {Config|Object} config
   */ constructor(el, config = {}){
        if (!(el instanceof HTMLElement)) {
            console.error("Invalid element", el);
            return;
        }
        INSTANCE_MAP.set(el, this);
        counter++;
        activeCounter++;
        this._searchInput = el;
        this._configure(config);
        // Private vars
        this._isMouse = false;
        this._preventInput = false;
        this._keyboardNavigation = false;
        this._searchFunc = debounce(()=>{
            this._loadFromServer(true);
        }, this._config.debounceTime);
        // Create html
        this._configureSearchInput();
        this._configureDropElement();
        if (this._config.fixed) {
            document.addEventListener("scroll", this, true);
            window.addEventListener("resize", this);
        }
        const clearControl = this._getClearControl();
        if (clearControl) clearControl.addEventListener("click", this);
        // Add listeners (remove then on dispose()). See handleEvent.
        [
            "focus",
            "change",
            "blur",
            "input",
            "keydown"
        ].forEach((type)=>{
            this._searchInput.addEventListener(type, this);
        });
        [
            "mousemove",
            "mouseleave"
        ].forEach((type)=>{
            this._dropElement.addEventListener(type, this);
        });
        this._fetchData();
    }
    // #region Core
    /**
   * Attach to all elements matched by the selector
   * @param {string} selector
   * @param {Config|Object} config
   */ static init(selector = "input.autocomplete", config = {}) {
        /**
     * @type {NodeListOf<HTMLInputElement>}
     */ const nodes = document.querySelectorAll(selector);
        nodes.forEach((el)=>{
            this.getOrCreateInstance(el, config);
        });
    }
    /**
   * @param {HTMLInputElement} el
   */ static getInstance(el) {
        return INSTANCE_MAP.has(el) ? INSTANCE_MAP.get(el) : null;
    }
    /**
   * @param {HTMLInputElement} el
   * @param {Object} config
   */ static getOrCreateInstance(el, config = {}) {
        return this.getInstance(el) || new this(el, config);
    }
    dispose() {
        activeCounter--;
        [
            "focus",
            "change",
            "blur",
            "input",
            "keydown"
        ].forEach((type)=>{
            this._searchInput.removeEventListener(type, this);
        });
        [
            "mousemove",
            "mouseleave"
        ].forEach((type)=>{
            this._dropElement.removeEventListener(type, this);
        });
        const clearControl = this._getClearControl();
        if (clearControl) clearControl.removeEventListener("click", this);
        // only remove if there are no more active elements
        if (this._config.fixed && activeCounter <= 0) {
            document.removeEventListener("scroll", this, true);
            window.removeEventListener("resize", this);
        }
        this._dropElement.parentElement.removeChild(this._dropElement);
        INSTANCE_MAP.delete(this._searchInput);
    }
    _getClearControl() {
        if (this._config.clearControl) return document.querySelector(this._config.clearControl);
    }
    /**
   * @link https://github.com/lifaon74/events-polyfill/issues/10
   * @link https://gist.github.com/WebReflection/ec9f6687842aa385477c4afca625bbf4#handling-events
   * @param {Event} event
   */ handleEvent = (event)=>{
        // debounce scroll and resize
        const debounced = [
            "scroll",
            "resize"
        ];
        if (debounced.includes(event.type)) {
            if (this._timer) window.cancelAnimationFrame(this._timer);
            this._timer = window.requestAnimationFrame(()=>{
                this[`on${event.type}`](event);
            });
        } else this[`on${event.type}`](event);
    };
    /**
   * @param {Config|Object} config
   */ _configure(config = {}) {
        this._config = Object.assign({}, DEFAULTS);
        // Handle options, using arguments first and data attr as override
        const o = {
            ...config,
            ...this._searchInput.dataset
        };
        // Allow 1/0, true/false as strings
        const parseBool = (value)=>[
                "true",
                "false",
                "1",
                "0",
                true,
                false
            ].includes(value) && !!JSON.parse(value);
        // Typecast provided options based on defaults types
        for (const [key, defaultValue] of Object.entries(DEFAULTS)){
            // Check for undefined keys
            if (o[key] === void 0) continue;
            const value = o[key];
            switch(typeof defaultValue){
                case "number":
                    this._config[key] = parseInt(value);
                    break;
                case "boolean":
                    this._config[key] = parseBool(value);
                    break;
                case "string":
                    this._config[key] = value.toString();
                    break;
                case "object":
                    // Arrays have a type object in js
                    if (Array.isArray(defaultValue)) {
                        if (typeof value === "string") {
                            const separator = value.includes("|") ? "|" : ",";
                            this._config[key] = value.split(separator);
                        } else this._config[key] = value;
                    } else this._config[key] = typeof value === "string" ? JSON.parse(value) : value;
                    break;
                case "function":
                    this._config[key] = typeof value === "string" ? window[value] : value;
                    break;
                default:
                    this._config[key] = value;
                    break;
            }
        }
    }
    // #endregion
    // #region Html
    _configureSearchInput() {
        this._searchInput.autocomplete = "off";
        this._searchInput.spellcheck = false;
        // note: firefox doesn't support the properties so we use attributes
        // @link https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-autocomplete
        // @link https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-expanded
        // use the aria-expanded state on the element with role combobox to communicate that the list is displayed.
        attrs(this._searchInput, {
            "aria-autocomplete": "list",
            "aria-haspopup": "menu",
            "aria-expanded": "false",
            role: "combobox"
        });
        // Even with autocomplete "off" we can get suggestion from browser due to label
        if (this._searchInput.id && this._config.preventBrowserAutocomplete) {
            const label = document.querySelector(`[for="${this._searchInput.id}"]`);
            if (label) zwijit(label);
        }
        // Hidden input?
        this._hiddenInput = null;
        if (this._config.hiddenInput) {
            this._hiddenInput = document.createElement("input");
            this._hiddenInput.type = "hidden";
            this._hiddenInput.value = this._config.hiddenValue;
            this._hiddenInput.name = this._searchInput.name;
            this._searchInput.name = "_" + this._searchInput.name;
            insertAfter(this._searchInput, this._hiddenInput);
        }
    }
    _configureDropElement() {
        this._dropElement = document.createElement("ul");
        this._dropElement.id = "ac-menu-" + counter;
        this._dropElement.classList.add(...[
            "dropdown-menu",
            "autocomplete-menu",
            "p-0"
        ]);
        this._dropElement.style.maxHeight = "280px";
        if (!this._config.fullWidth) this._dropElement.style.maxWidth = "360px";
        if (this._config.fixed) this._dropElement.style.position = "fixed";
        this._dropElement.style.overflowY = "auto";
        // Prevent scrolling the menu from scrolling the page
        // @link https://developer.mozilla.org/en-US/docs/Web/CSS/overscroll-behavior
        this._dropElement.style.overscrollBehavior = "contain";
        this._dropElement.style.textAlign = "unset"; // otherwise RTL is not good
        insertAfter(this._searchInput, this._dropElement);
        // include aria-controls with the value of the id of the suggested list of values.
        this._searchInput.setAttribute("aria-controls", this._dropElement.id);
    }
    // #endregion
    // #region Events
    onclick(e) {
        if (e.target.matches(this._config.clearControl)) this.clear();
    }
    oninput(e) {
        if (this._preventInput) return;
        // Input has changed, clear value
        if (this._hiddenInput) this._hiddenInput.value = null;
        this.showOrSearch();
    }
    onchange(e) {
        const search = this._searchInput.value;
        const item = Object.values(this._items).find((item)=>item.label === search);
        this._config.onChange(item, this);
    }
    onblur(e) {
        // Clicking on the scroll in a modal blur the element incorrectly
        if (this._isMouse && e.relatedTarget && e.relatedTarget.classList.contains("modal")) {
            // Set focus back in
            this._searchInput.focus();
            return;
        }
        setTimeout(()=>{
            this.hideSuggestions();
        }, 100);
    }
    onfocus(e) {
        this.showOrSearch();
    }
    /**
   * keypress doesn't send arrow keys, so we use keydown
   * @param {KeyboardEvent} e
   */ onkeydown(e) {
        const key = e.keyCode || e.key;
        switch(key){
            case 13:
            case "Enter":
                if (this.isDropdownVisible()) {
                    const selection = this.getSelection();
                    if (selection) selection.click();
                    if (selection || !this._config.ignoreEnter) e.preventDefault();
                }
                break;
            case 38:
            case "ArrowUp":
                e.preventDefault();
                this._keyboardNavigation = true;
                this._moveSelection(PREV);
                break;
            case 40:
            case "ArrowDown":
                e.preventDefault();
                this._keyboardNavigation = true;
                if (this.isDropdownVisible()) this._moveSelection(NEXT);
                else // show menu regardless of input length
                this.showOrSearch(false);
                break;
            case 27:
            case "Escape":
                if (this.isDropdownVisible()) {
                    this._searchInput.focus();
                    this.hideSuggestions();
                }
                break;
        }
    }
    onmousemove(e) {
        this._isMouse = true;
        // Moving the mouse means no longer using keyboard
        this._keyboardNavigation = false;
    }
    onmouseleave(e) {
        this._isMouse = false;
        // Remove selection
        this.removeSelection();
    }
    onscroll(e) {
        this._positionMenu();
    }
    onresize(e) {
        this._positionMenu();
    }
    // #endregion
    // #region Api
    /**
   * @param {String} k
   * @returns {Config}
   */ getConfig(k = null) {
        if (k !== null) return this._config[k];
        return this._config;
    }
    /**
   * @param {String} k
   * @param {*} v
   */ setConfig(k, v) {
        this._config[k] = v;
    }
    setData(src) {
        this._items = {};
        this._addItems(src);
    }
    enable() {
        this._searchInput.setAttribute("disabled", "");
    }
    disable() {
        this._searchInput.removeAttribute("disabled");
    }
    /**
   * @returns {boolean}
   */ isDisabled() {
        return this._searchInput.hasAttribute("disabled") || this._searchInput.disabled || this._searchInput.hasAttribute("readonly");
    }
    /**
   * @returns {boolean}
   */ isDropdownVisible() {
        return this._dropElement.classList.contains(SHOW_CLASS);
    }
    clear() {
        this._searchInput.value = "";
        if (this._hiddenInput) this._hiddenInput.value = "";
    }
    // #endregion
    // #region Selection management
    /**
   * @returns {HTMLElement}
   */ getSelection() {
        return this._dropElement.querySelector("a." + ACTIVE_CLASS);
    }
    removeSelection() {
        const selection = this.getSelection();
        if (selection) selection.classList.remove(...this._activeClasses());
    }
    /**
   * @returns {Array}
   */ _activeClasses() {
        return [
            ...this._config.activeClasses,
            ACTIVE_CLASS
        ];
    }
    /**
   * @param {HTMLElement} li
   * @returns {Boolean}
   */ _isItemEnabled(li) {
        if (li.style.display === "none") return false;
        const fc = li.firstElementChild;
        return fc.tagName === "A" && !fc.classList.contains("disabled");
    }
    /**
   * @param {String} dir
   * @param {*|HTMLElement} sel
   * @returns {HTMLElement}
   */ _moveSelection(dir = NEXT, sel = null) {
        const active = this.getSelection();
        // select first li
        if (!active) {
            // no active selection, cannot go back
            if (dir === PREV) return sel;
            // find first enabled item
            if (!sel) {
                sel = this._dropElement.firstChild;
                while(sel && !this._isItemEnabled(sel))sel = sel["nextSibling"];
            }
        } else {
            const sibling = dir === NEXT ? "nextSibling" : "previousSibling";
            // Iterate over enabled li
            sel = active.parentNode;
            do sel = sel[sibling];
            while (sel && !this._isItemEnabled(sel));
            // We have a new selection
            if (sel) {
                // Change classes
                active.classList.remove(...this._activeClasses());
                // Scroll if necessary
                if (dir === PREV) // Don't use scrollIntoView as it scrolls the whole window
                sel.parentNode.scrollTop = sel.offsetTop - sel.parentNode.offsetTop;
                else // This is the equivalent of scrollIntoView(false) but only for parent node
                if (sel.offsetTop > sel.parentNode.offsetHeight - sel.offsetHeight) sel.parentNode.scrollTop += sel.offsetHeight;
            } else if (active) sel = active.parentElement;
        }
        if (sel) {
            const a = sel.querySelector("a");
            a.classList.add(...this._activeClasses());
            this._searchInput.setAttribute("aria-activedescendant", a.id);
            if (this._config.updateOnSelect) this._searchInput.value = a.dataset.label;
        } else this._searchInput.setAttribute("aria-activedescendant", "");
        return sel;
    }
    // #endregion
    // #region Implementation
    /**
   * Do we have enough input to show suggestions ?
   * @returns {Boolean}
   */ _shouldShow() {
        if (this.isDisabled()) return false;
        return this._searchInput.value.length >= this._config.suggestionsThreshold;
    }
    /**
   * Show suggestions or load them
   * @param {Boolean} check
   */ showOrSearch(check = true) {
        if (check && !this._shouldShow()) {
            this.hideSuggestions();
            return;
        }
        if (this._config.liveServer) this._searchFunc();
        else if (this._config.source) this._config.source(this._searchInput.value, (items)=>{
            this.setData(items);
            this._showSuggestions();
        });
        else this._showSuggestions();
    }
    /**
   * @param {String} name
   * @returns {HTMLElement}
   */ _createGroup(name) {
        const newChild = this._createLi();
        const newChildSpan = document.createElement("span");
        newChild.append(newChildSpan);
        newChildSpan.classList.add(...[
            "dropdown-header",
            "text-truncate"
        ]);
        newChildSpan.innerHTML = name;
        return newChild;
    }
    /**
   * @param {String} lookup
   * @param {Object} item
   * @returns {HTMLElement}
   */ _createItem(lookup, item) {
        let label = item.label;
        if (this._config.highlightTyped) {
            const idx = normalize(label).indexOf(lookup);
            if (idx !== -1) label = label.substring(0, idx) + `<mark class="${this._config.highlightClass}">${label.substring(idx, idx + lookup.length)}</mark>` + label.substring(idx + lookup.length, label.length);
        }
        label = this._config.onRenderItem(item, label, this);
        const newChild = this._createLi();
        const newChildLink = document.createElement("a");
        newChild.append(newChildLink);
        newChildLink.id = this._dropElement.id + "-" + this._dropElement.children.length;
        newChildLink.classList.add(...[
            "dropdown-item",
            "text-truncate"
        ]);
        if (this._config.itemClass) newChildLink.classList.add(...this._config.itemClass.split(" "));
        newChildLink.setAttribute("data-value", item.value);
        newChildLink.setAttribute("data-label", item.label);
        // Behave like a datalist (tab doesn't allow item selection)
        // @link https://developer.mozilla.org/en-US/docs/Web/HTML/Element/datalist
        newChildLink.setAttribute("tabindex", "-1");
        newChildLink.setAttribute("role", "menuitem");
        newChildLink.setAttribute("href", "#");
        newChildLink.innerHTML = label;
        if (item.data) for (const [key, value] of Object.entries(item.data))newChildLink.dataset[key] = value;
        if (this._config.fillIn) {
            const fillIn = document.createElement("button");
            fillIn.type = "button"; // prevent submit
            fillIn.classList.add(...[
                "btn",
                "btn-link",
                "border-0"
            ]);
            fillIn.innerHTML = `<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
      <path fill-rule="evenodd" d="M2 2.5a.5.5 0 0 1 .5-.5h6a.5.5 0 0 1 0 1H3.707l10.147 10.146a.5.5 0 0 1-.708.708L3 3.707V8.5a.5.5 0 0 1-1 0z"/>
      </svg>`;
            newChild.append(fillIn);
            newChild.classList.add(...[
                "d-flex",
                "justify-content-between"
            ]);
            fillIn.addEventListener("click", (event)=>{
                this._searchInput.value = item.label;
                this._searchInput.focus(); // focus back to keep editing
            });
        }
        // Hover sets active item
        newChildLink.addEventListener("mouseenter", (event)=>{
            // Don't trigger enter if using arrows or not currently using the mouse
            if (this._keyboardNavigation || !this._isMouse) return;
            this.removeSelection();
            newChild.querySelector("a").classList.add(...this._activeClasses());
        });
        // Prevent searchInput losing focus and close the menu
        newChildLink.addEventListener("mousedown", (event)=>{
            event.preventDefault();
        });
        // Apply value
        newChildLink.addEventListener("click", (event)=>{
            event.preventDefault();
            // Prevent input otherwise it might trigger autocomplete due to value change
            this._preventInput = true;
            this._searchInput.value = decodeHtml(item.label);
            // Populate value in hidden input
            if (this._hiddenInput) this._hiddenInput.value = item.value;
            this._config.onSelectItem(item, this);
            this.hideSuggestions();
            this._preventInput = false;
        });
        return newChild;
    }
    /**
   * Show drop menu with suggestions
   */ _showSuggestions() {
        // It's not focused anymore
        if (document.activeElement != this._searchInput) return;
        const lookup = normalize(this._searchInput.value);
        this._dropElement.innerHTML = "";
        const keys = Object.keys(this._items);
        let count = 0;
        let firstItem = null;
        const groups = [];
        for(let i = 0; i < keys.length; i++){
            const key = keys[i];
            const entry = this._items[key];
            // Check search length since we can trigger dropdown with arrow
            const showAllSuggestions = this._config.showAllSuggestions || lookup.length === 0;
            // Do we find a matching string or do we display immediately ?
            let isMatched = lookup.length == 0 && this._config.suggestionsThreshold === 0;
            if (!showAllSuggestions && lookup.length > 0) // match on any field
            this._config.searchFields.forEach((sf)=>{
                const text = normalize(entry[sf]);
                let found = false;
                if (this._config.fuzzy) found = fuzzyMatch(text, lookup);
                else {
                    const idx = text.indexOf(lookup);
                    found = this._config.startsWith ? idx === 0 : idx >= 0;
                }
                if (found) isMatched = true;
            });
            const selectFirst = isMatched || lookup.length === 0;
            if (showAllSuggestions || isMatched) {
                count++;
                // Group
                if (entry.group && !groups.includes(entry.group)) {
                    const newItem = this._createGroup(entry.group);
                    this._dropElement.appendChild(newItem);
                    groups.push(entry.group);
                }
                const newItem = this._createItem(lookup, entry);
                // Only select as first item if its matching or no lookup
                if (!firstItem && selectFirst) firstItem = newItem;
                this._dropElement.appendChild(newItem);
                if (this._config.maximumItems > 0 && count >= this._config.maximumItems) break;
            }
        }
        if (firstItem && this._config.autoselectFirst) {
            this.removeSelection();
            this._moveSelection(NEXT, firstItem);
        }
        if (count === 0) {
            if (this._config.notFoundMessage) {
                const newChild = this._createLi();
                newChild.innerHTML = `<span class="dropdown-item">${this._config.notFoundMessage}</span>`;
                this._dropElement.appendChild(newChild);
                this._showDropdown();
            } else // Remove dropdown if not found
            this.hideSuggestions();
        } else // Or show it if necessary
        this._showDropdown();
    }
    /**
   * @returns {HTMLLIElement}
   */ _createLi() {
        const newChild = document.createElement("li");
        newChild.setAttribute("role", "presentation");
        return newChild;
    }
    /**
   * Show and position dropdown
   */ _showDropdown() {
        this._dropElement.classList.add(SHOW_CLASS);
        // Register role when shown to avoid empty children issues
        this._dropElement.setAttribute("role", "menu");
        attrs(this._searchInput, {
            "aria-expanded": "true"
        });
        this._positionMenu();
    }
    /**
   * Show or hide suggestions
   * @param {Boolean} check
   */ toggleSuggestions(check = true) {
        if (this._dropElement.classList.contains(SHOW_CLASS)) this.hideSuggestions();
        else this.showOrSearch(check);
    }
    /**
   * Hide the dropdown menu
   */ hideSuggestions() {
        this._dropElement.classList.remove(SHOW_CLASS);
        attrs(this._searchInput, {
            "aria-expanded": "false"
        });
        this.removeSelection();
    }
    /**
   * @returns {HTMLInputElement}
   */ getInput() {
        return this._searchInput;
    }
    /**
   * @returns {HTMLUListElement}
   */ getDropMenu() {
        return this._dropElement;
    }
    /**
   * Position the dropdown menu
   */ _positionMenu() {
        const styles = window.getComputedStyle(this._searchInput);
        const bounds = this._searchInput.getBoundingClientRect();
        const isRTL = styles.direction === "rtl";
        const fullWidth = this._config.fullWidth;
        const fixed = this._config.fixed;
        // Don't position left if not fixed since it may not work in all situations
        // due to offsetParent margin or in tables
        let left = null;
        let top = null;
        if (fixed) {
            left = bounds.x;
            top = bounds.y + bounds.height;
            // Align end
            if (isRTL && !fullWidth) left -= this._dropElement.offsetWidth - bounds.width;
        }
        // Reset any height overflow adjustement
        this._dropElement.style.transform = "unset";
        // Use full holder width
        if (fullWidth) this._dropElement.style.width = this._searchInput.offsetWidth + "px";
        // Position element
        if (left !== null) this._dropElement.style.left = left + "px";
        if (top !== null) this._dropElement.style.top = top + "px";
        // Overflow height
        const dropBounds = this._dropElement.getBoundingClientRect();
        const h = window.innerHeight;
        // We display above input if it overflows
        if (dropBounds.y + dropBounds.height > h) {
            // We need to add the offset twice
            const topOffset = fullWidth ? bounds.height + 4 : bounds.height;
            // In chrome, we need 100.1% to avoid blurry text
            // @link https://stackoverflow.com/questions/32034574/font-looks-blurry-after-translate-in-chrome
            this._dropElement.style.transform = "translateY(calc(-100.1% - " + topOffset + "px))";
        }
    }
    _fetchData() {
        this._items = {};
        // From an array of items or an object
        this._addItems(this._config.items);
        // From a datalist
        const dl = this._config.datalist;
        if (dl) {
            const datalist = document.querySelector(`#${dl}`);
            if (datalist) {
                const items = Array.from(datalist.children).map((o)=>{
                    const value = o.getAttribute("value") ?? o.innerHTML.toLowerCase();
                    const label = o.innerHTML;
                    return {
                        value,
                        label
                    };
                });
                this._addItems(items);
            } else console.error(`Datalist not found ${dl}`);
        }
        this._setHiddenVal();
        // From an external source
        if (this._config.server && !this._config.liveServer) this._loadFromServer();
    }
    _setHiddenVal() {
        if (this._config.hiddenInput && !this._config.hiddenValue) {
            for (const [value, entry] of Object.entries(this._items))if (entry.label == this._searchInput.value) this._hiddenInput.value = value;
        }
    }
    /**
   * @param {Array|Object} src An array of items or a value:label object
   */ _addItems(src) {
        const keys = Object.keys(src);
        for(let i = 0; i < keys.length; i++){
            const key = keys[i];
            const entry = src[key];
            if (entry.group && entry.items) {
                entry.items.forEach((e)=>e.group = entry.group);
                this._addItems(entry.items);
                continue;
            }
            const label = typeof entry === "string" ? entry : entry.label;
            const item = typeof entry !== "object" ? {} : entry;
            // Normalize entry
            item.label = entry[this._config.labelField] ?? label;
            item.value = entry[this._config.valueField] ?? key;
            // Make sure we have a label
            if (item.label) this._items[item.value] = item;
        }
    }
    /**
   * @param {boolean} show
   */ _loadFromServer(show = false) {
        if (this._abortController) this._abortController.abort();
        this._abortController = new AbortController();
        // Read data params dynamically as well
        let extraParams = this._searchInput.dataset.serverParams || {};
        if (typeof extraParams == "string") extraParams = JSON.parse(extraParams);
        const params = Object.assign({}, this._config.serverParams, extraParams);
        // Pass current value
        params[this._config.queryParam] = this._searchInput.value;
        // Prevent caching
        if (this._config.noCache) params.t = Date.now();
        // We have a related field
        if (params.related) {
            /**
       * @type {HTMLInputElement}
       */ //@ts-ignore
            const input = document.getElementById(params.related);
            if (input) {
                params.related = input.value;
                const inputName = input.getAttribute("name");
                if (inputName) params[inputName] = input.value;
            }
        }
        const urlParams = new URLSearchParams(params);
        let url = this._config.server;
        let fetchOptions = Object.assign(this._config.fetchOptions, {
            method: this._config.serverMethod || "GET",
            signal: this._abortController.signal
        });
        if (fetchOptions.method === "POST") fetchOptions.body = urlParams;
        else url += "?" + urlParams.toString();
        this._searchInput.classList.add(LOADING_CLASS);
        this._config.onBeforeFetch(this);
        fetch(url, fetchOptions).then((r)=>this._config.onServerResponse(r, this)).then((suggestions)=>{
            const data = nested(this._config.serverDataKey, suggestions) || suggestions;
            this.setData(data);
            this._setHiddenVal();
            this._abortController = null;
            if (show) this._showSuggestions();
        }).catch((e)=>{
            this._config.onServerError(e, this._abortController.signal, this);
        }).finally((e)=>{
            this._searchInput.classList.remove(LOADING_CLASS);
            this._config.onAfterFetch(this);
        });
    }
}
exports.default = Autocomplete;

},{"@parcel/transformer-js/src/esmodule-helpers.js":"gkKU3"}],"gkKU3":[function(require,module,exports) {
exports.interopDefault = function(a) {
    return a && a.__esModule ? a : {
        default: a
    };
};
exports.defineInteropFlag = function(a) {
    Object.defineProperty(a, "__esModule", {
        value: true
    });
};
exports.exportAll = function(source, dest) {
    Object.keys(source).forEach(function(key) {
        if (key === "default" || key === "__esModule" || Object.prototype.hasOwnProperty.call(dest, key)) return;
        Object.defineProperty(dest, key, {
            enumerable: true,
            get: function() {
                return source[key];
            }
        });
    });
    return dest;
};
exports.export = function(dest, destName, get) {
    Object.defineProperty(dest, destName, {
        enumerable: true,
        get: get
    });
};

},{}]},["lNrhS","9RRD0"], "9RRD0", "parcelRequire94c2")

//# sourceMappingURL=admin.js.map
