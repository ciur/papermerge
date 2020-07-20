/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = 0);
/******/ })
/************************************************************************/
/******/ ({

/***/ "./node_modules/backbone/backbone.js":
/*!*******************************************!*\
  !*** ./node_modules/backbone/backbone.js ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/* WEBPACK VAR INJECTION */(function(global) {var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;//     Backbone.js 1.4.0

//     (c) 2010-2019 Jeremy Ashkenas and DocumentCloud
//     Backbone may be freely distributed under the MIT license.
//     For all details and documentation:
//     http://backbonejs.org

(function(factory) {

  // Establish the root object, `window` (`self`) in the browser, or `global` on the server.
  // We use `self` instead of `window` for `WebWorker` support.
  var root = typeof self == 'object' && self.self === self && self ||
            typeof global == 'object' && global.global === global && global;

  // Set up Backbone appropriately for the environment. Start with AMD.
  if (true) {
    !(__WEBPACK_AMD_DEFINE_ARRAY__ = [__webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js"), __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), exports], __WEBPACK_AMD_DEFINE_RESULT__ = (function(_, $, exports) {
      // Export global even in AMD case in case this script is loaded with
      // others that may still expect a global Backbone.
      root.Backbone = factory(root, exports, _, $);
    }).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

  // Next for Node.js or CommonJS. jQuery may not be needed as a module.
  } else { var _, $; }

})(function(root, Backbone, _, $) {

  // Initial Setup
  // -------------

  // Save the previous value of the `Backbone` variable, so that it can be
  // restored later on, if `noConflict` is used.
  var previousBackbone = root.Backbone;

  // Create a local reference to a common array method we'll want to use later.
  var slice = Array.prototype.slice;

  // Current version of the library. Keep in sync with `package.json`.
  Backbone.VERSION = '1.4.0';

  // For Backbone's purposes, jQuery, Zepto, Ender, or My Library (kidding) owns
  // the `$` variable.
  Backbone.$ = $;

  // Runs Backbone.js in *noConflict* mode, returning the `Backbone` variable
  // to its previous owner. Returns a reference to this Backbone object.
  Backbone.noConflict = function() {
    root.Backbone = previousBackbone;
    return this;
  };

  // Turn on `emulateHTTP` to support legacy HTTP servers. Setting this option
  // will fake `"PATCH"`, `"PUT"` and `"DELETE"` requests via the `_method` parameter and
  // set a `X-Http-Method-Override` header.
  Backbone.emulateHTTP = false;

  // Turn on `emulateJSON` to support legacy servers that can't deal with direct
  // `application/json` requests ... this will encode the body as
  // `application/x-www-form-urlencoded` instead and will send the model in a
  // form param named `model`.
  Backbone.emulateJSON = false;

  // Backbone.Events
  // ---------------

  // A module that can be mixed in to *any object* in order to provide it with
  // a custom event channel. You may bind a callback to an event with `on` or
  // remove with `off`; `trigger`-ing an event fires all callbacks in
  // succession.
  //
  //     var object = {};
  //     _.extend(object, Backbone.Events);
  //     object.on('expand', function(){ alert('expanded'); });
  //     object.trigger('expand');
  //
  var Events = Backbone.Events = {};

  // Regular expression used to split event strings.
  var eventSplitter = /\s+/;

  // A private global variable to share between listeners and listenees.
  var _listening;

  // Iterates over the standard `event, callback` (as well as the fancy multiple
  // space-separated events `"change blur", callback` and jQuery-style event
  // maps `{event: callback}`).
  var eventsApi = function(iteratee, events, name, callback, opts) {
    var i = 0, names;
    if (name && typeof name === 'object') {
      // Handle event maps.
      if (callback !== void 0 && 'context' in opts && opts.context === void 0) opts.context = callback;
      for (names = _.keys(name); i < names.length ; i++) {
        events = eventsApi(iteratee, events, names[i], name[names[i]], opts);
      }
    } else if (name && eventSplitter.test(name)) {
      // Handle space-separated event names by delegating them individually.
      for (names = name.split(eventSplitter); i < names.length; i++) {
        events = iteratee(events, names[i], callback, opts);
      }
    } else {
      // Finally, standard events.
      events = iteratee(events, name, callback, opts);
    }
    return events;
  };

  // Bind an event to a `callback` function. Passing `"all"` will bind
  // the callback to all events fired.
  Events.on = function(name, callback, context) {
    this._events = eventsApi(onApi, this._events || {}, name, callback, {
      context: context,
      ctx: this,
      listening: _listening
    });

    if (_listening) {
      var listeners = this._listeners || (this._listeners = {});
      listeners[_listening.id] = _listening;
      // Allow the listening to use a counter, instead of tracking
      // callbacks for library interop
      _listening.interop = false;
    }

    return this;
  };

  // Inversion-of-control versions of `on`. Tell *this* object to listen to
  // an event in another object... keeping track of what it's listening to
  // for easier unbinding later.
  Events.listenTo = function(obj, name, callback) {
    if (!obj) return this;
    var id = obj._listenId || (obj._listenId = _.uniqueId('l'));
    var listeningTo = this._listeningTo || (this._listeningTo = {});
    var listening = _listening = listeningTo[id];

    // This object is not listening to any other events on `obj` yet.
    // Setup the necessary references to track the listening callbacks.
    if (!listening) {
      this._listenId || (this._listenId = _.uniqueId('l'));
      listening = _listening = listeningTo[id] = new Listening(this, obj);
    }

    // Bind callbacks on obj.
    var error = tryCatchOn(obj, name, callback, this);
    _listening = void 0;

    if (error) throw error;
    // If the target obj is not Backbone.Events, track events manually.
    if (listening.interop) listening.on(name, callback);

    return this;
  };

  // The reducing API that adds a callback to the `events` object.
  var onApi = function(events, name, callback, options) {
    if (callback) {
      var handlers = events[name] || (events[name] = []);
      var context = options.context, ctx = options.ctx, listening = options.listening;
      if (listening) listening.count++;

      handlers.push({callback: callback, context: context, ctx: context || ctx, listening: listening});
    }
    return events;
  };

  // An try-catch guarded #on function, to prevent poisoning the global
  // `_listening` variable.
  var tryCatchOn = function(obj, name, callback, context) {
    try {
      obj.on(name, callback, context);
    } catch (e) {
      return e;
    }
  };

  // Remove one or many callbacks. If `context` is null, removes all
  // callbacks with that function. If `callback` is null, removes all
  // callbacks for the event. If `name` is null, removes all bound
  // callbacks for all events.
  Events.off = function(name, callback, context) {
    if (!this._events) return this;
    this._events = eventsApi(offApi, this._events, name, callback, {
      context: context,
      listeners: this._listeners
    });

    return this;
  };

  // Tell this object to stop listening to either specific events ... or
  // to every object it's currently listening to.
  Events.stopListening = function(obj, name, callback) {
    var listeningTo = this._listeningTo;
    if (!listeningTo) return this;

    var ids = obj ? [obj._listenId] : _.keys(listeningTo);
    for (var i = 0; i < ids.length; i++) {
      var listening = listeningTo[ids[i]];

      // If listening doesn't exist, this object is not currently
      // listening to obj. Break out early.
      if (!listening) break;

      listening.obj.off(name, callback, this);
      if (listening.interop) listening.off(name, callback);
    }
    if (_.isEmpty(listeningTo)) this._listeningTo = void 0;

    return this;
  };

  // The reducing API that removes a callback from the `events` object.
  var offApi = function(events, name, callback, options) {
    if (!events) return;

    var context = options.context, listeners = options.listeners;
    var i = 0, names;

    // Delete all event listeners and "drop" events.
    if (!name && !context && !callback) {
      for (names = _.keys(listeners); i < names.length; i++) {
        listeners[names[i]].cleanup();
      }
      return;
    }

    names = name ? [name] : _.keys(events);
    for (; i < names.length; i++) {
      name = names[i];
      var handlers = events[name];

      // Bail out if there are no events stored.
      if (!handlers) break;

      // Find any remaining events.
      var remaining = [];
      for (var j = 0; j < handlers.length; j++) {
        var handler = handlers[j];
        if (
          callback && callback !== handler.callback &&
            callback !== handler.callback._callback ||
              context && context !== handler.context
        ) {
          remaining.push(handler);
        } else {
          var listening = handler.listening;
          if (listening) listening.off(name, callback);
        }
      }

      // Replace events if there are any remaining.  Otherwise, clean up.
      if (remaining.length) {
        events[name] = remaining;
      } else {
        delete events[name];
      }
    }

    return events;
  };

  // Bind an event to only be triggered a single time. After the first time
  // the callback is invoked, its listener will be removed. If multiple events
  // are passed in using the space-separated syntax, the handler will fire
  // once for each event, not once for a combination of all events.
  Events.once = function(name, callback, context) {
    // Map the event into a `{event: once}` object.
    var events = eventsApi(onceMap, {}, name, callback, this.off.bind(this));
    if (typeof name === 'string' && context == null) callback = void 0;
    return this.on(events, callback, context);
  };

  // Inversion-of-control versions of `once`.
  Events.listenToOnce = function(obj, name, callback) {
    // Map the event into a `{event: once}` object.
    var events = eventsApi(onceMap, {}, name, callback, this.stopListening.bind(this, obj));
    return this.listenTo(obj, events);
  };

  // Reduces the event callbacks into a map of `{event: onceWrapper}`.
  // `offer` unbinds the `onceWrapper` after it has been called.
  var onceMap = function(map, name, callback, offer) {
    if (callback) {
      var once = map[name] = _.once(function() {
        offer(name, once);
        callback.apply(this, arguments);
      });
      once._callback = callback;
    }
    return map;
  };

  // Trigger one or many events, firing all bound callbacks. Callbacks are
  // passed the same arguments as `trigger` is, apart from the event name
  // (unless you're listening on `"all"`, which will cause your callback to
  // receive the true name of the event as the first argument).
  Events.trigger = function(name) {
    if (!this._events) return this;

    var length = Math.max(0, arguments.length - 1);
    var args = Array(length);
    for (var i = 0; i < length; i++) args[i] = arguments[i + 1];

    eventsApi(triggerApi, this._events, name, void 0, args);
    return this;
  };

  // Handles triggering the appropriate event callbacks.
  var triggerApi = function(objEvents, name, callback, args) {
    if (objEvents) {
      var events = objEvents[name];
      var allEvents = objEvents.all;
      if (events && allEvents) allEvents = allEvents.slice();
      if (events) triggerEvents(events, args);
      if (allEvents) triggerEvents(allEvents, [name].concat(args));
    }
    return objEvents;
  };

  // A difficult-to-believe, but optimized internal dispatch function for
  // triggering events. Tries to keep the usual cases speedy (most internal
  // Backbone events have 3 arguments).
  var triggerEvents = function(events, args) {
    var ev, i = -1, l = events.length, a1 = args[0], a2 = args[1], a3 = args[2];
    switch (args.length) {
      case 0: while (++i < l) (ev = events[i]).callback.call(ev.ctx); return;
      case 1: while (++i < l) (ev = events[i]).callback.call(ev.ctx, a1); return;
      case 2: while (++i < l) (ev = events[i]).callback.call(ev.ctx, a1, a2); return;
      case 3: while (++i < l) (ev = events[i]).callback.call(ev.ctx, a1, a2, a3); return;
      default: while (++i < l) (ev = events[i]).callback.apply(ev.ctx, args); return;
    }
  };

  // A listening class that tracks and cleans up memory bindings
  // when all callbacks have been offed.
  var Listening = function(listener, obj) {
    this.id = listener._listenId;
    this.listener = listener;
    this.obj = obj;
    this.interop = true;
    this.count = 0;
    this._events = void 0;
  };

  Listening.prototype.on = Events.on;

  // Offs a callback (or several).
  // Uses an optimized counter if the listenee uses Backbone.Events.
  // Otherwise, falls back to manual tracking to support events
  // library interop.
  Listening.prototype.off = function(name, callback) {
    var cleanup;
    if (this.interop) {
      this._events = eventsApi(offApi, this._events, name, callback, {
        context: void 0,
        listeners: void 0
      });
      cleanup = !this._events;
    } else {
      this.count--;
      cleanup = this.count === 0;
    }
    if (cleanup) this.cleanup();
  };

  // Cleans up memory bindings between the listener and the listenee.
  Listening.prototype.cleanup = function() {
    delete this.listener._listeningTo[this.obj._listenId];
    if (!this.interop) delete this.obj._listeners[this.id];
  };

  // Aliases for backwards compatibility.
  Events.bind   = Events.on;
  Events.unbind = Events.off;

  // Allow the `Backbone` object to serve as a global event bus, for folks who
  // want global "pubsub" in a convenient place.
  _.extend(Backbone, Events);

  // Backbone.Model
  // --------------

  // Backbone **Models** are the basic data object in the framework --
  // frequently representing a row in a table in a database on your server.
  // A discrete chunk of data and a bunch of useful, related methods for
  // performing computations and transformations on that data.

  // Create a new model with the specified attributes. A client id (`cid`)
  // is automatically generated and assigned for you.
  var Model = Backbone.Model = function(attributes, options) {
    var attrs = attributes || {};
    options || (options = {});
    this.preinitialize.apply(this, arguments);
    this.cid = _.uniqueId(this.cidPrefix);
    this.attributes = {};
    if (options.collection) this.collection = options.collection;
    if (options.parse) attrs = this.parse(attrs, options) || {};
    var defaults = _.result(this, 'defaults');
    attrs = _.defaults(_.extend({}, defaults, attrs), defaults);
    this.set(attrs, options);
    this.changed = {};
    this.initialize.apply(this, arguments);
  };

  // Attach all inheritable methods to the Model prototype.
  _.extend(Model.prototype, Events, {

    // A hash of attributes whose current and previous value differ.
    changed: null,

    // The value returned during the last failed validation.
    validationError: null,

    // The default name for the JSON `id` attribute is `"id"`. MongoDB and
    // CouchDB users may want to set this to `"_id"`.
    idAttribute: 'id',

    // The prefix is used to create the client id which is used to identify models locally.
    // You may want to override this if you're experiencing name clashes with model ids.
    cidPrefix: 'c',

    // preinitialize is an empty function by default. You can override it with a function
    // or object.  preinitialize will run before any instantiation logic is run in the Model.
    preinitialize: function(){},

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // Return a copy of the model's `attributes` object.
    toJSON: function(options) {
      return _.clone(this.attributes);
    },

    // Proxy `Backbone.sync` by default -- but override this if you need
    // custom syncing semantics for *this* particular model.
    sync: function() {
      return Backbone.sync.apply(this, arguments);
    },

    // Get the value of an attribute.
    get: function(attr) {
      return this.attributes[attr];
    },

    // Get the HTML-escaped value of an attribute.
    escape: function(attr) {
      return _.escape(this.get(attr));
    },

    // Returns `true` if the attribute contains a value that is not null
    // or undefined.
    has: function(attr) {
      return this.get(attr) != null;
    },

    // Special-cased proxy to underscore's `_.matches` method.
    matches: function(attrs) {
      return !!_.iteratee(attrs, this)(this.attributes);
    },

    // Set a hash of model attributes on the object, firing `"change"`. This is
    // the core primitive operation of a model, updating the data and notifying
    // anyone who needs to know about the change in state. The heart of the beast.
    set: function(key, val, options) {
      if (key == null) return this;

      // Handle both `"key", value` and `{key: value}` -style arguments.
      var attrs;
      if (typeof key === 'object') {
        attrs = key;
        options = val;
      } else {
        (attrs = {})[key] = val;
      }

      options || (options = {});

      // Run validation.
      if (!this._validate(attrs, options)) return false;

      // Extract attributes and options.
      var unset      = options.unset;
      var silent     = options.silent;
      var changes    = [];
      var changing   = this._changing;
      this._changing = true;

      if (!changing) {
        this._previousAttributes = _.clone(this.attributes);
        this.changed = {};
      }

      var current = this.attributes;
      var changed = this.changed;
      var prev    = this._previousAttributes;

      // For each `set` attribute, update or delete the current value.
      for (var attr in attrs) {
        val = attrs[attr];
        if (!_.isEqual(current[attr], val)) changes.push(attr);
        if (!_.isEqual(prev[attr], val)) {
          changed[attr] = val;
        } else {
          delete changed[attr];
        }
        unset ? delete current[attr] : current[attr] = val;
      }

      // Update the `id`.
      if (this.idAttribute in attrs) this.id = this.get(this.idAttribute);

      // Trigger all relevant attribute changes.
      if (!silent) {
        if (changes.length) this._pending = options;
        for (var i = 0; i < changes.length; i++) {
          this.trigger('change:' + changes[i], this, current[changes[i]], options);
        }
      }

      // You might be wondering why there's a `while` loop here. Changes can
      // be recursively nested within `"change"` events.
      if (changing) return this;
      if (!silent) {
        while (this._pending) {
          options = this._pending;
          this._pending = false;
          this.trigger('change', this, options);
        }
      }
      this._pending = false;
      this._changing = false;
      return this;
    },

    // Remove an attribute from the model, firing `"change"`. `unset` is a noop
    // if the attribute doesn't exist.
    unset: function(attr, options) {
      return this.set(attr, void 0, _.extend({}, options, {unset: true}));
    },

    // Clear all attributes on the model, firing `"change"`.
    clear: function(options) {
      var attrs = {};
      for (var key in this.attributes) attrs[key] = void 0;
      return this.set(attrs, _.extend({}, options, {unset: true}));
    },

    // Determine if the model has changed since the last `"change"` event.
    // If you specify an attribute name, determine if that attribute has changed.
    hasChanged: function(attr) {
      if (attr == null) return !_.isEmpty(this.changed);
      return _.has(this.changed, attr);
    },

    // Return an object containing all the attributes that have changed, or
    // false if there are no changed attributes. Useful for determining what
    // parts of a view need to be updated and/or what attributes need to be
    // persisted to the server. Unset attributes will be set to undefined.
    // You can also pass an attributes object to diff against the model,
    // determining if there *would be* a change.
    changedAttributes: function(diff) {
      if (!diff) return this.hasChanged() ? _.clone(this.changed) : false;
      var old = this._changing ? this._previousAttributes : this.attributes;
      var changed = {};
      var hasChanged;
      for (var attr in diff) {
        var val = diff[attr];
        if (_.isEqual(old[attr], val)) continue;
        changed[attr] = val;
        hasChanged = true;
      }
      return hasChanged ? changed : false;
    },

    // Get the previous value of an attribute, recorded at the time the last
    // `"change"` event was fired.
    previous: function(attr) {
      if (attr == null || !this._previousAttributes) return null;
      return this._previousAttributes[attr];
    },

    // Get all of the attributes of the model at the time of the previous
    // `"change"` event.
    previousAttributes: function() {
      return _.clone(this._previousAttributes);
    },

    // Fetch the model from the server, merging the response with the model's
    // local attributes. Any changed attributes will trigger a "change" event.
    fetch: function(options) {
      options = _.extend({parse: true}, options);
      var model = this;
      var success = options.success;
      options.success = function(resp) {
        var serverAttrs = options.parse ? model.parse(resp, options) : resp;
        if (!model.set(serverAttrs, options)) return false;
        if (success) success.call(options.context, model, resp, options);
        model.trigger('sync', model, resp, options);
      };
      wrapError(this, options);
      return this.sync('read', this, options);
    },

    // Set a hash of model attributes, and sync the model to the server.
    // If the server returns an attributes hash that differs, the model's
    // state will be `set` again.
    save: function(key, val, options) {
      // Handle both `"key", value` and `{key: value}` -style arguments.
      var attrs;
      if (key == null || typeof key === 'object') {
        attrs = key;
        options = val;
      } else {
        (attrs = {})[key] = val;
      }

      options = _.extend({validate: true, parse: true}, options);
      var wait = options.wait;

      // If we're not waiting and attributes exist, save acts as
      // `set(attr).save(null, opts)` with validation. Otherwise, check if
      // the model will be valid when the attributes, if any, are set.
      if (attrs && !wait) {
        if (!this.set(attrs, options)) return false;
      } else if (!this._validate(attrs, options)) {
        return false;
      }

      // After a successful server-side save, the client is (optionally)
      // updated with the server-side state.
      var model = this;
      var success = options.success;
      var attributes = this.attributes;
      options.success = function(resp) {
        // Ensure attributes are restored during synchronous saves.
        model.attributes = attributes;
        var serverAttrs = options.parse ? model.parse(resp, options) : resp;
        if (wait) serverAttrs = _.extend({}, attrs, serverAttrs);
        if (serverAttrs && !model.set(serverAttrs, options)) return false;
        if (success) success.call(options.context, model, resp, options);
        model.trigger('sync', model, resp, options);
      };
      wrapError(this, options);

      // Set temporary attributes if `{wait: true}` to properly find new ids.
      if (attrs && wait) this.attributes = _.extend({}, attributes, attrs);

      var method = this.isNew() ? 'create' : options.patch ? 'patch' : 'update';
      if (method === 'patch' && !options.attrs) options.attrs = attrs;
      var xhr = this.sync(method, this, options);

      // Restore attributes.
      this.attributes = attributes;

      return xhr;
    },

    // Destroy this model on the server if it was already persisted.
    // Optimistically removes the model from its collection, if it has one.
    // If `wait: true` is passed, waits for the server to respond before removal.
    destroy: function(options) {
      options = options ? _.clone(options) : {};
      var model = this;
      var success = options.success;
      var wait = options.wait;

      var destroy = function() {
        model.stopListening();
        model.trigger('destroy', model, model.collection, options);
      };

      options.success = function(resp) {
        if (wait) destroy();
        if (success) success.call(options.context, model, resp, options);
        if (!model.isNew()) model.trigger('sync', model, resp, options);
      };

      var xhr = false;
      if (this.isNew()) {
        _.defer(options.success);
      } else {
        wrapError(this, options);
        xhr = this.sync('delete', this, options);
      }
      if (!wait) destroy();
      return xhr;
    },

    // Default URL for the model's representation on the server -- if you're
    // using Backbone's restful methods, override this to change the endpoint
    // that will be called.
    url: function() {
      var base =
        _.result(this, 'urlRoot') ||
        _.result(this.collection, 'url') ||
        urlError();
      if (this.isNew()) return base;
      var id = this.get(this.idAttribute);
      return base.replace(/[^\/]$/, '$&/') + encodeURIComponent(id);
    },

    // **parse** converts a response into the hash of attributes to be `set` on
    // the model. The default implementation is just to pass the response along.
    parse: function(resp, options) {
      return resp;
    },

    // Create a new model with identical attributes to this one.
    clone: function() {
      return new this.constructor(this.attributes);
    },

    // A model is new if it has never been saved to the server, and lacks an id.
    isNew: function() {
      return !this.has(this.idAttribute);
    },

    // Check if the model is currently in a valid state.
    isValid: function(options) {
      return this._validate({}, _.extend({}, options, {validate: true}));
    },

    // Run validation against the next complete set of model attributes,
    // returning `true` if all is well. Otherwise, fire an `"invalid"` event.
    _validate: function(attrs, options) {
      if (!options.validate || !this.validate) return true;
      attrs = _.extend({}, this.attributes, attrs);
      var error = this.validationError = this.validate(attrs, options) || null;
      if (!error) return true;
      this.trigger('invalid', this, error, _.extend(options, {validationError: error}));
      return false;
    }

  });

  // Backbone.Collection
  // -------------------

  // If models tend to represent a single row of data, a Backbone Collection is
  // more analogous to a table full of data ... or a small slice or page of that
  // table, or a collection of rows that belong together for a particular reason
  // -- all of the messages in this particular folder, all of the documents
  // belonging to this particular author, and so on. Collections maintain
  // indexes of their models, both in order, and for lookup by `id`.

  // Create a new **Collection**, perhaps to contain a specific type of `model`.
  // If a `comparator` is specified, the Collection will maintain
  // its models in sort order, as they're added and removed.
  var Collection = Backbone.Collection = function(models, options) {
    options || (options = {});
    this.preinitialize.apply(this, arguments);
    if (options.model) this.model = options.model;
    if (options.comparator !== void 0) this.comparator = options.comparator;
    this._reset();
    this.initialize.apply(this, arguments);
    if (models) this.reset(models, _.extend({silent: true}, options));
  };

  // Default options for `Collection#set`.
  var setOptions = {add: true, remove: true, merge: true};
  var addOptions = {add: true, remove: false};

  // Splices `insert` into `array` at index `at`.
  var splice = function(array, insert, at) {
    at = Math.min(Math.max(at, 0), array.length);
    var tail = Array(array.length - at);
    var length = insert.length;
    var i;
    for (i = 0; i < tail.length; i++) tail[i] = array[i + at];
    for (i = 0; i < length; i++) array[i + at] = insert[i];
    for (i = 0; i < tail.length; i++) array[i + length + at] = tail[i];
  };

  // Define the Collection's inheritable methods.
  _.extend(Collection.prototype, Events, {

    // The default model for a collection is just a **Backbone.Model**.
    // This should be overridden in most cases.
    model: Model,


    // preinitialize is an empty function by default. You can override it with a function
    // or object.  preinitialize will run before any instantiation logic is run in the Collection.
    preinitialize: function(){},

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // The JSON representation of a Collection is an array of the
    // models' attributes.
    toJSON: function(options) {
      return this.map(function(model) { return model.toJSON(options); });
    },

    // Proxy `Backbone.sync` by default.
    sync: function() {
      return Backbone.sync.apply(this, arguments);
    },

    // Add a model, or list of models to the set. `models` may be Backbone
    // Models or raw JavaScript objects to be converted to Models, or any
    // combination of the two.
    add: function(models, options) {
      return this.set(models, _.extend({merge: false}, options, addOptions));
    },

    // Remove a model, or a list of models from the set.
    remove: function(models, options) {
      options = _.extend({}, options);
      var singular = !_.isArray(models);
      models = singular ? [models] : models.slice();
      var removed = this._removeModels(models, options);
      if (!options.silent && removed.length) {
        options.changes = {added: [], merged: [], removed: removed};
        this.trigger('update', this, options);
      }
      return singular ? removed[0] : removed;
    },

    // Update a collection by `set`-ing a new list of models, adding new ones,
    // removing models that are no longer present, and merging models that
    // already exist in the collection, as necessary. Similar to **Model#set**,
    // the core operation for updating the data contained by the collection.
    set: function(models, options) {
      if (models == null) return;

      options = _.extend({}, setOptions, options);
      if (options.parse && !this._isModel(models)) {
        models = this.parse(models, options) || [];
      }

      var singular = !_.isArray(models);
      models = singular ? [models] : models.slice();

      var at = options.at;
      if (at != null) at = +at;
      if (at > this.length) at = this.length;
      if (at < 0) at += this.length + 1;

      var set = [];
      var toAdd = [];
      var toMerge = [];
      var toRemove = [];
      var modelMap = {};

      var add = options.add;
      var merge = options.merge;
      var remove = options.remove;

      var sort = false;
      var sortable = this.comparator && at == null && options.sort !== false;
      var sortAttr = _.isString(this.comparator) ? this.comparator : null;

      // Turn bare objects into model references, and prevent invalid models
      // from being added.
      var model, i;
      for (i = 0; i < models.length; i++) {
        model = models[i];

        // If a duplicate is found, prevent it from being added and
        // optionally merge it into the existing model.
        var existing = this.get(model);
        if (existing) {
          if (merge && model !== existing) {
            var attrs = this._isModel(model) ? model.attributes : model;
            if (options.parse) attrs = existing.parse(attrs, options);
            existing.set(attrs, options);
            toMerge.push(existing);
            if (sortable && !sort) sort = existing.hasChanged(sortAttr);
          }
          if (!modelMap[existing.cid]) {
            modelMap[existing.cid] = true;
            set.push(existing);
          }
          models[i] = existing;

        // If this is a new, valid model, push it to the `toAdd` list.
        } else if (add) {
          model = models[i] = this._prepareModel(model, options);
          if (model) {
            toAdd.push(model);
            this._addReference(model, options);
            modelMap[model.cid] = true;
            set.push(model);
          }
        }
      }

      // Remove stale models.
      if (remove) {
        for (i = 0; i < this.length; i++) {
          model = this.models[i];
          if (!modelMap[model.cid]) toRemove.push(model);
        }
        if (toRemove.length) this._removeModels(toRemove, options);
      }

      // See if sorting is needed, update `length` and splice in new models.
      var orderChanged = false;
      var replace = !sortable && add && remove;
      if (set.length && replace) {
        orderChanged = this.length !== set.length || _.some(this.models, function(m, index) {
          return m !== set[index];
        });
        this.models.length = 0;
        splice(this.models, set, 0);
        this.length = this.models.length;
      } else if (toAdd.length) {
        if (sortable) sort = true;
        splice(this.models, toAdd, at == null ? this.length : at);
        this.length = this.models.length;
      }

      // Silently sort the collection if appropriate.
      if (sort) this.sort({silent: true});

      // Unless silenced, it's time to fire all appropriate add/sort/update events.
      if (!options.silent) {
        for (i = 0; i < toAdd.length; i++) {
          if (at != null) options.index = at + i;
          model = toAdd[i];
          model.trigger('add', model, this, options);
        }
        if (sort || orderChanged) this.trigger('sort', this, options);
        if (toAdd.length || toRemove.length || toMerge.length) {
          options.changes = {
            added: toAdd,
            removed: toRemove,
            merged: toMerge
          };
          this.trigger('update', this, options);
        }
      }

      // Return the added (or merged) model (or models).
      return singular ? models[0] : models;
    },

    // When you have more items than you want to add or remove individually,
    // you can reset the entire set with a new list of models, without firing
    // any granular `add` or `remove` events. Fires `reset` when finished.
    // Useful for bulk operations and optimizations.
    reset: function(models, options) {
      options = options ? _.clone(options) : {};
      for (var i = 0; i < this.models.length; i++) {
        this._removeReference(this.models[i], options);
      }
      options.previousModels = this.models;
      this._reset();
      models = this.add(models, _.extend({silent: true}, options));
      if (!options.silent) this.trigger('reset', this, options);
      return models;
    },

    // Add a model to the end of the collection.
    push: function(model, options) {
      return this.add(model, _.extend({at: this.length}, options));
    },

    // Remove a model from the end of the collection.
    pop: function(options) {
      var model = this.at(this.length - 1);
      return this.remove(model, options);
    },

    // Add a model to the beginning of the collection.
    unshift: function(model, options) {
      return this.add(model, _.extend({at: 0}, options));
    },

    // Remove a model from the beginning of the collection.
    shift: function(options) {
      var model = this.at(0);
      return this.remove(model, options);
    },

    // Slice out a sub-array of models from the collection.
    slice: function() {
      return slice.apply(this.models, arguments);
    },

    // Get a model from the set by id, cid, model object with id or cid
    // properties, or an attributes object that is transformed through modelId.
    get: function(obj) {
      if (obj == null) return void 0;
      return this._byId[obj] ||
        this._byId[this.modelId(this._isModel(obj) ? obj.attributes : obj)] ||
        obj.cid && this._byId[obj.cid];
    },

    // Returns `true` if the model is in the collection.
    has: function(obj) {
      return this.get(obj) != null;
    },

    // Get the model at the given index.
    at: function(index) {
      if (index < 0) index += this.length;
      return this.models[index];
    },

    // Return models with matching attributes. Useful for simple cases of
    // `filter`.
    where: function(attrs, first) {
      return this[first ? 'find' : 'filter'](attrs);
    },

    // Return the first model with matching attributes. Useful for simple cases
    // of `find`.
    findWhere: function(attrs) {
      return this.where(attrs, true);
    },

    // Force the collection to re-sort itself. You don't need to call this under
    // normal circumstances, as the set will maintain sort order as each item
    // is added.
    sort: function(options) {
      var comparator = this.comparator;
      if (!comparator) throw new Error('Cannot sort a set without a comparator');
      options || (options = {});

      var length = comparator.length;
      if (_.isFunction(comparator)) comparator = comparator.bind(this);

      // Run sort based on type of `comparator`.
      if (length === 1 || _.isString(comparator)) {
        this.models = this.sortBy(comparator);
      } else {
        this.models.sort(comparator);
      }
      if (!options.silent) this.trigger('sort', this, options);
      return this;
    },

    // Pluck an attribute from each model in the collection.
    pluck: function(attr) {
      return this.map(attr + '');
    },

    // Fetch the default set of models for this collection, resetting the
    // collection when they arrive. If `reset: true` is passed, the response
    // data will be passed through the `reset` method instead of `set`.
    fetch: function(options) {
      options = _.extend({parse: true}, options);
      var success = options.success;
      var collection = this;
      options.success = function(resp) {
        var method = options.reset ? 'reset' : 'set';
        collection[method](resp, options);
        if (success) success.call(options.context, collection, resp, options);
        collection.trigger('sync', collection, resp, options);
      };
      wrapError(this, options);
      return this.sync('read', this, options);
    },

    // Create a new instance of a model in this collection. Add the model to the
    // collection immediately, unless `wait: true` is passed, in which case we
    // wait for the server to agree.
    create: function(model, options) {
      options = options ? _.clone(options) : {};
      var wait = options.wait;
      model = this._prepareModel(model, options);
      if (!model) return false;
      if (!wait) this.add(model, options);
      var collection = this;
      var success = options.success;
      options.success = function(m, resp, callbackOpts) {
        if (wait) collection.add(m, callbackOpts);
        if (success) success.call(callbackOpts.context, m, resp, callbackOpts);
      };
      model.save(null, options);
      return model;
    },

    // **parse** converts a response into a list of models to be added to the
    // collection. The default implementation is just to pass it through.
    parse: function(resp, options) {
      return resp;
    },

    // Create a new collection with an identical list of models as this one.
    clone: function() {
      return new this.constructor(this.models, {
        model: this.model,
        comparator: this.comparator
      });
    },

    // Define how to uniquely identify models in the collection.
    modelId: function(attrs) {
      return attrs[this.model.prototype.idAttribute || 'id'];
    },

    // Get an iterator of all models in this collection.
    values: function() {
      return new CollectionIterator(this, ITERATOR_VALUES);
    },

    // Get an iterator of all model IDs in this collection.
    keys: function() {
      return new CollectionIterator(this, ITERATOR_KEYS);
    },

    // Get an iterator of all [ID, model] tuples in this collection.
    entries: function() {
      return new CollectionIterator(this, ITERATOR_KEYSVALUES);
    },

    // Private method to reset all internal state. Called when the collection
    // is first initialized or reset.
    _reset: function() {
      this.length = 0;
      this.models = [];
      this._byId  = {};
    },

    // Prepare a hash of attributes (or other model) to be added to this
    // collection.
    _prepareModel: function(attrs, options) {
      if (this._isModel(attrs)) {
        if (!attrs.collection) attrs.collection = this;
        return attrs;
      }
      options = options ? _.clone(options) : {};
      options.collection = this;
      var model = new this.model(attrs, options);
      if (!model.validationError) return model;
      this.trigger('invalid', this, model.validationError, options);
      return false;
    },

    // Internal method called by both remove and set.
    _removeModels: function(models, options) {
      var removed = [];
      for (var i = 0; i < models.length; i++) {
        var model = this.get(models[i]);
        if (!model) continue;

        var index = this.indexOf(model);
        this.models.splice(index, 1);
        this.length--;

        // Remove references before triggering 'remove' event to prevent an
        // infinite loop. #3693
        delete this._byId[model.cid];
        var id = this.modelId(model.attributes);
        if (id != null) delete this._byId[id];

        if (!options.silent) {
          options.index = index;
          model.trigger('remove', model, this, options);
        }

        removed.push(model);
        this._removeReference(model, options);
      }
      return removed;
    },

    // Method for checking whether an object should be considered a model for
    // the purposes of adding to the collection.
    _isModel: function(model) {
      return model instanceof Model;
    },

    // Internal method to create a model's ties to a collection.
    _addReference: function(model, options) {
      this._byId[model.cid] = model;
      var id = this.modelId(model.attributes);
      if (id != null) this._byId[id] = model;
      model.on('all', this._onModelEvent, this);
    },

    // Internal method to sever a model's ties to a collection.
    _removeReference: function(model, options) {
      delete this._byId[model.cid];
      var id = this.modelId(model.attributes);
      if (id != null) delete this._byId[id];
      if (this === model.collection) delete model.collection;
      model.off('all', this._onModelEvent, this);
    },

    // Internal method called every time a model in the set fires an event.
    // Sets need to update their indexes when models change ids. All other
    // events simply proxy through. "add" and "remove" events that originate
    // in other collections are ignored.
    _onModelEvent: function(event, model, collection, options) {
      if (model) {
        if ((event === 'add' || event === 'remove') && collection !== this) return;
        if (event === 'destroy') this.remove(model, options);
        if (event === 'change') {
          var prevId = this.modelId(model.previousAttributes());
          var id = this.modelId(model.attributes);
          if (prevId !== id) {
            if (prevId != null) delete this._byId[prevId];
            if (id != null) this._byId[id] = model;
          }
        }
      }
      this.trigger.apply(this, arguments);
    }

  });

  // Defining an @@iterator method implements JavaScript's Iterable protocol.
  // In modern ES2015 browsers, this value is found at Symbol.iterator.
  /* global Symbol */
  var $$iterator = typeof Symbol === 'function' && Symbol.iterator;
  if ($$iterator) {
    Collection.prototype[$$iterator] = Collection.prototype.values;
  }

  // CollectionIterator
  // ------------------

  // A CollectionIterator implements JavaScript's Iterator protocol, allowing the
  // use of `for of` loops in modern browsers and interoperation between
  // Backbone.Collection and other JavaScript functions and third-party libraries
  // which can operate on Iterables.
  var CollectionIterator = function(collection, kind) {
    this._collection = collection;
    this._kind = kind;
    this._index = 0;
  };

  // This "enum" defines the three possible kinds of values which can be emitted
  // by a CollectionIterator that correspond to the values(), keys() and entries()
  // methods on Collection, respectively.
  var ITERATOR_VALUES = 1;
  var ITERATOR_KEYS = 2;
  var ITERATOR_KEYSVALUES = 3;

  // All Iterators should themselves be Iterable.
  if ($$iterator) {
    CollectionIterator.prototype[$$iterator] = function() {
      return this;
    };
  }

  CollectionIterator.prototype.next = function() {
    if (this._collection) {

      // Only continue iterating if the iterated collection is long enough.
      if (this._index < this._collection.length) {
        var model = this._collection.at(this._index);
        this._index++;

        // Construct a value depending on what kind of values should be iterated.
        var value;
        if (this._kind === ITERATOR_VALUES) {
          value = model;
        } else {
          var id = this._collection.modelId(model.attributes);
          if (this._kind === ITERATOR_KEYS) {
            value = id;
          } else { // ITERATOR_KEYSVALUES
            value = [id, model];
          }
        }
        return {value: value, done: false};
      }

      // Once exhausted, remove the reference to the collection so future
      // calls to the next method always return done.
      this._collection = void 0;
    }

    return {value: void 0, done: true};
  };

  // Backbone.View
  // -------------

  // Backbone Views are almost more convention than they are actual code. A View
  // is simply a JavaScript object that represents a logical chunk of UI in the
  // DOM. This might be a single item, an entire list, a sidebar or panel, or
  // even the surrounding frame which wraps your whole app. Defining a chunk of
  // UI as a **View** allows you to define your DOM events declaratively, without
  // having to worry about render order ... and makes it easy for the view to
  // react to specific changes in the state of your models.

  // Creating a Backbone.View creates its initial element outside of the DOM,
  // if an existing element is not provided...
  var View = Backbone.View = function(options) {
    this.cid = _.uniqueId('view');
    this.preinitialize.apply(this, arguments);
    _.extend(this, _.pick(options, viewOptions));
    this._ensureElement();
    this.initialize.apply(this, arguments);
  };

  // Cached regex to split keys for `delegate`.
  var delegateEventSplitter = /^(\S+)\s*(.*)$/;

  // List of view options to be set as properties.
  var viewOptions = ['model', 'collection', 'el', 'id', 'attributes', 'className', 'tagName', 'events'];

  // Set up all inheritable **Backbone.View** properties and methods.
  _.extend(View.prototype, Events, {

    // The default `tagName` of a View's element is `"div"`.
    tagName: 'div',

    // jQuery delegate for element lookup, scoped to DOM elements within the
    // current view. This should be preferred to global lookups where possible.
    $: function(selector) {
      return this.$el.find(selector);
    },

    // preinitialize is an empty function by default. You can override it with a function
    // or object.  preinitialize will run before any instantiation logic is run in the View
    preinitialize: function(){},

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // **render** is the core function that your view should override, in order
    // to populate its element (`this.el`), with the appropriate HTML. The
    // convention is for **render** to always return `this`.
    render: function() {
      return this;
    },

    // Remove this view by taking the element out of the DOM, and removing any
    // applicable Backbone.Events listeners.
    remove: function() {
      this._removeElement();
      this.stopListening();
      return this;
    },

    // Remove this view's element from the document and all event listeners
    // attached to it. Exposed for subclasses using an alternative DOM
    // manipulation API.
    _removeElement: function() {
      this.$el.remove();
    },

    // Change the view's element (`this.el` property) and re-delegate the
    // view's events on the new element.
    setElement: function(element) {
      this.undelegateEvents();
      this._setElement(element);
      this.delegateEvents();
      return this;
    },

    // Creates the `this.el` and `this.$el` references for this view using the
    // given `el`. `el` can be a CSS selector or an HTML string, a jQuery
    // context or an element. Subclasses can override this to utilize an
    // alternative DOM manipulation API and are only required to set the
    // `this.el` property.
    _setElement: function(el) {
      this.$el = el instanceof Backbone.$ ? el : Backbone.$(el);
      this.el = this.$el[0];
    },

    // Set callbacks, where `this.events` is a hash of
    //
    // *{"event selector": "callback"}*
    //
    //     {
    //       'mousedown .title':  'edit',
    //       'click .button':     'save',
    //       'click .open':       function(e) { ... }
    //     }
    //
    // pairs. Callbacks will be bound to the view, with `this` set properly.
    // Uses event delegation for efficiency.
    // Omitting the selector binds the event to `this.el`.
    delegateEvents: function(events) {
      events || (events = _.result(this, 'events'));
      if (!events) return this;
      this.undelegateEvents();
      for (var key in events) {
        var method = events[key];
        if (!_.isFunction(method)) method = this[method];
        if (!method) continue;
        var match = key.match(delegateEventSplitter);
        this.delegate(match[1], match[2], method.bind(this));
      }
      return this;
    },

    // Add a single event listener to the view's element (or a child element
    // using `selector`). This only works for delegate-able events: not `focus`,
    // `blur`, and not `change`, `submit`, and `reset` in Internet Explorer.
    delegate: function(eventName, selector, listener) {
      this.$el.on(eventName + '.delegateEvents' + this.cid, selector, listener);
      return this;
    },

    // Clears all callbacks previously bound to the view by `delegateEvents`.
    // You usually don't need to use this, but may wish to if you have multiple
    // Backbone views attached to the same DOM element.
    undelegateEvents: function() {
      if (this.$el) this.$el.off('.delegateEvents' + this.cid);
      return this;
    },

    // A finer-grained `undelegateEvents` for removing a single delegated event.
    // `selector` and `listener` are both optional.
    undelegate: function(eventName, selector, listener) {
      this.$el.off(eventName + '.delegateEvents' + this.cid, selector, listener);
      return this;
    },

    // Produces a DOM element to be assigned to your view. Exposed for
    // subclasses using an alternative DOM manipulation API.
    _createElement: function(tagName) {
      return document.createElement(tagName);
    },

    // Ensure that the View has a DOM element to render into.
    // If `this.el` is a string, pass it through `$()`, take the first
    // matching element, and re-assign it to `el`. Otherwise, create
    // an element from the `id`, `className` and `tagName` properties.
    _ensureElement: function() {
      if (!this.el) {
        var attrs = _.extend({}, _.result(this, 'attributes'));
        if (this.id) attrs.id = _.result(this, 'id');
        if (this.className) attrs['class'] = _.result(this, 'className');
        this.setElement(this._createElement(_.result(this, 'tagName')));
        this._setAttributes(attrs);
      } else {
        this.setElement(_.result(this, 'el'));
      }
    },

    // Set attributes from a hash on this view's element.  Exposed for
    // subclasses using an alternative DOM manipulation API.
    _setAttributes: function(attributes) {
      this.$el.attr(attributes);
    }

  });

  // Proxy Backbone class methods to Underscore functions, wrapping the model's
  // `attributes` object or collection's `models` array behind the scenes.
  //
  // collection.filter(function(model) { return model.get('age') > 10 });
  // collection.each(this.addView);
  //
  // `Function#apply` can be slow so we use the method's arg count, if we know it.
  var addMethod = function(base, length, method, attribute) {
    switch (length) {
      case 1: return function() {
        return base[method](this[attribute]);
      };
      case 2: return function(value) {
        return base[method](this[attribute], value);
      };
      case 3: return function(iteratee, context) {
        return base[method](this[attribute], cb(iteratee, this), context);
      };
      case 4: return function(iteratee, defaultVal, context) {
        return base[method](this[attribute], cb(iteratee, this), defaultVal, context);
      };
      default: return function() {
        var args = slice.call(arguments);
        args.unshift(this[attribute]);
        return base[method].apply(base, args);
      };
    }
  };

  var addUnderscoreMethods = function(Class, base, methods, attribute) {
    _.each(methods, function(length, method) {
      if (base[method]) Class.prototype[method] = addMethod(base, length, method, attribute);
    });
  };

  // Support `collection.sortBy('attr')` and `collection.findWhere({id: 1})`.
  var cb = function(iteratee, instance) {
    if (_.isFunction(iteratee)) return iteratee;
    if (_.isObject(iteratee) && !instance._isModel(iteratee)) return modelMatcher(iteratee);
    if (_.isString(iteratee)) return function(model) { return model.get(iteratee); };
    return iteratee;
  };
  var modelMatcher = function(attrs) {
    var matcher = _.matches(attrs);
    return function(model) {
      return matcher(model.attributes);
    };
  };

  // Underscore methods that we want to implement on the Collection.
  // 90% of the core usefulness of Backbone Collections is actually implemented
  // right here:
  var collectionMethods = {forEach: 3, each: 3, map: 3, collect: 3, reduce: 0,
    foldl: 0, inject: 0, reduceRight: 0, foldr: 0, find: 3, detect: 3, filter: 3,
    select: 3, reject: 3, every: 3, all: 3, some: 3, any: 3, include: 3, includes: 3,
    contains: 3, invoke: 0, max: 3, min: 3, toArray: 1, size: 1, first: 3,
    head: 3, take: 3, initial: 3, rest: 3, tail: 3, drop: 3, last: 3,
    without: 0, difference: 0, indexOf: 3, shuffle: 1, lastIndexOf: 3,
    isEmpty: 1, chain: 1, sample: 3, partition: 3, groupBy: 3, countBy: 3,
    sortBy: 3, indexBy: 3, findIndex: 3, findLastIndex: 3};


  // Underscore methods that we want to implement on the Model, mapped to the
  // number of arguments they take.
  var modelMethods = {keys: 1, values: 1, pairs: 1, invert: 1, pick: 0,
    omit: 0, chain: 1, isEmpty: 1};

  // Mix in each Underscore method as a proxy to `Collection#models`.

  _.each([
    [Collection, collectionMethods, 'models'],
    [Model, modelMethods, 'attributes']
  ], function(config) {
    var Base = config[0],
        methods = config[1],
        attribute = config[2];

    Base.mixin = function(obj) {
      var mappings = _.reduce(_.functions(obj), function(memo, name) {
        memo[name] = 0;
        return memo;
      }, {});
      addUnderscoreMethods(Base, obj, mappings, attribute);
    };

    addUnderscoreMethods(Base, _, methods, attribute);
  });

  // Backbone.sync
  // -------------

  // Override this function to change the manner in which Backbone persists
  // models to the server. You will be passed the type of request, and the
  // model in question. By default, makes a RESTful Ajax request
  // to the model's `url()`. Some possible customizations could be:
  //
  // * Use `setTimeout` to batch rapid-fire updates into a single request.
  // * Send up the models as XML instead of JSON.
  // * Persist models via WebSockets instead of Ajax.
  //
  // Turn on `Backbone.emulateHTTP` in order to send `PUT` and `DELETE` requests
  // as `POST`, with a `_method` parameter containing the true HTTP method,
  // as well as all requests with the body as `application/x-www-form-urlencoded`
  // instead of `application/json` with the model in a param named `model`.
  // Useful when interfacing with server-side languages like **PHP** that make
  // it difficult to read the body of `PUT` requests.
  Backbone.sync = function(method, model, options) {
    var type = methodMap[method];

    // Default options, unless specified.
    _.defaults(options || (options = {}), {
      emulateHTTP: Backbone.emulateHTTP,
      emulateJSON: Backbone.emulateJSON
    });

    // Default JSON-request options.
    var params = {type: type, dataType: 'json'};

    // Ensure that we have a URL.
    if (!options.url) {
      params.url = _.result(model, 'url') || urlError();
    }

    // Ensure that we have the appropriate request data.
    if (options.data == null && model && (method === 'create' || method === 'update' || method === 'patch')) {
      params.contentType = 'application/json';
      params.data = JSON.stringify(options.attrs || model.toJSON(options));
    }

    // For older servers, emulate JSON by encoding the request into an HTML-form.
    if (options.emulateJSON) {
      params.contentType = 'application/x-www-form-urlencoded';
      params.data = params.data ? {model: params.data} : {};
    }

    // For older servers, emulate HTTP by mimicking the HTTP method with `_method`
    // And an `X-HTTP-Method-Override` header.
    if (options.emulateHTTP && (type === 'PUT' || type === 'DELETE' || type === 'PATCH')) {
      params.type = 'POST';
      if (options.emulateJSON) params.data._method = type;
      var beforeSend = options.beforeSend;
      options.beforeSend = function(xhr) {
        xhr.setRequestHeader('X-HTTP-Method-Override', type);
        if (beforeSend) return beforeSend.apply(this, arguments);
      };
    }

    // Don't process data on a non-GET request.
    if (params.type !== 'GET' && !options.emulateJSON) {
      params.processData = false;
    }

    // Pass along `textStatus` and `errorThrown` from jQuery.
    var error = options.error;
    options.error = function(xhr, textStatus, errorThrown) {
      options.textStatus = textStatus;
      options.errorThrown = errorThrown;
      if (error) error.call(options.context, xhr, textStatus, errorThrown);
    };

    // Make the request, allowing the user to override any Ajax options.
    var xhr = options.xhr = Backbone.ajax(_.extend(params, options));
    model.trigger('request', model, xhr, options);
    return xhr;
  };

  // Map from CRUD to HTTP for our default `Backbone.sync` implementation.
  var methodMap = {
    create: 'POST',
    update: 'PUT',
    patch: 'PATCH',
    delete: 'DELETE',
    read: 'GET'
  };

  // Set the default implementation of `Backbone.ajax` to proxy through to `$`.
  // Override this if you'd like to use a different library.
  Backbone.ajax = function() {
    return Backbone.$.ajax.apply(Backbone.$, arguments);
  };

  // Backbone.Router
  // ---------------

  // Routers map faux-URLs to actions, and fire events when routes are
  // matched. Creating a new one sets its `routes` hash, if not set statically.
  var Router = Backbone.Router = function(options) {
    options || (options = {});
    this.preinitialize.apply(this, arguments);
    if (options.routes) this.routes = options.routes;
    this._bindRoutes();
    this.initialize.apply(this, arguments);
  };

  // Cached regular expressions for matching named param parts and splatted
  // parts of route strings.
  var optionalParam = /\((.*?)\)/g;
  var namedParam    = /(\(\?)?:\w+/g;
  var splatParam    = /\*\w+/g;
  var escapeRegExp  = /[\-{}\[\]+?.,\\\^$|#\s]/g;

  // Set up all inheritable **Backbone.Router** properties and methods.
  _.extend(Router.prototype, Events, {

    // preinitialize is an empty function by default. You can override it with a function
    // or object.  preinitialize will run before any instantiation logic is run in the Router.
    preinitialize: function(){},

    // Initialize is an empty function by default. Override it with your own
    // initialization logic.
    initialize: function(){},

    // Manually bind a single named route to a callback. For example:
    //
    //     this.route('search/:query/p:num', 'search', function(query, num) {
    //       ...
    //     });
    //
    route: function(route, name, callback) {
      if (!_.isRegExp(route)) route = this._routeToRegExp(route);
      if (_.isFunction(name)) {
        callback = name;
        name = '';
      }
      if (!callback) callback = this[name];
      var router = this;
      Backbone.history.route(route, function(fragment) {
        var args = router._extractParameters(route, fragment);
        if (router.execute(callback, args, name) !== false) {
          router.trigger.apply(router, ['route:' + name].concat(args));
          router.trigger('route', name, args);
          Backbone.history.trigger('route', router, name, args);
        }
      });
      return this;
    },

    // Execute a route handler with the provided parameters.  This is an
    // excellent place to do pre-route setup or post-route cleanup.
    execute: function(callback, args, name) {
      if (callback) callback.apply(this, args);
    },

    // Simple proxy to `Backbone.history` to save a fragment into the history.
    navigate: function(fragment, options) {
      Backbone.history.navigate(fragment, options);
      return this;
    },

    // Bind all defined routes to `Backbone.history`. We have to reverse the
    // order of the routes here to support behavior where the most general
    // routes can be defined at the bottom of the route map.
    _bindRoutes: function() {
      if (!this.routes) return;
      this.routes = _.result(this, 'routes');
      var route, routes = _.keys(this.routes);
      while ((route = routes.pop()) != null) {
        this.route(route, this.routes[route]);
      }
    },

    // Convert a route string into a regular expression, suitable for matching
    // against the current location hash.
    _routeToRegExp: function(route) {
      route = route.replace(escapeRegExp, '\\$&')
        .replace(optionalParam, '(?:$1)?')
        .replace(namedParam, function(match, optional) {
          return optional ? match : '([^/?]+)';
        })
        .replace(splatParam, '([^?]*?)');
      return new RegExp('^' + route + '(?:\\?([\\s\\S]*))?$');
    },

    // Given a route, and a URL fragment that it matches, return the array of
    // extracted decoded parameters. Empty or unmatched parameters will be
    // treated as `null` to normalize cross-browser behavior.
    _extractParameters: function(route, fragment) {
      var params = route.exec(fragment).slice(1);
      return _.map(params, function(param, i) {
        // Don't decode the search params.
        if (i === params.length - 1) return param || null;
        return param ? decodeURIComponent(param) : null;
      });
    }

  });

  // Backbone.History
  // ----------------

  // Handles cross-browser history management, based on either
  // [pushState](http://diveintohtml5.info/history.html) and real URLs, or
  // [onhashchange](https://developer.mozilla.org/en-US/docs/DOM/window.onhashchange)
  // and URL fragments. If the browser supports neither (old IE, natch),
  // falls back to polling.
  var History = Backbone.History = function() {
    this.handlers = [];
    this.checkUrl = this.checkUrl.bind(this);

    // Ensure that `History` can be used outside of the browser.
    if (typeof window !== 'undefined') {
      this.location = window.location;
      this.history = window.history;
    }
  };

  // Cached regex for stripping a leading hash/slash and trailing space.
  var routeStripper = /^[#\/]|\s+$/g;

  // Cached regex for stripping leading and trailing slashes.
  var rootStripper = /^\/+|\/+$/g;

  // Cached regex for stripping urls of hash.
  var pathStripper = /#.*$/;

  // Has the history handling already been started?
  History.started = false;

  // Set up all inheritable **Backbone.History** properties and methods.
  _.extend(History.prototype, Events, {

    // The default interval to poll for hash changes, if necessary, is
    // twenty times a second.
    interval: 50,

    // Are we at the app root?
    atRoot: function() {
      var path = this.location.pathname.replace(/[^\/]$/, '$&/');
      return path === this.root && !this.getSearch();
    },

    // Does the pathname match the root?
    matchRoot: function() {
      var path = this.decodeFragment(this.location.pathname);
      var rootPath = path.slice(0, this.root.length - 1) + '/';
      return rootPath === this.root;
    },

    // Unicode characters in `location.pathname` are percent encoded so they're
    // decoded for comparison. `%25` should not be decoded since it may be part
    // of an encoded parameter.
    decodeFragment: function(fragment) {
      return decodeURI(fragment.replace(/%25/g, '%2525'));
    },

    // In IE6, the hash fragment and search params are incorrect if the
    // fragment contains `?`.
    getSearch: function() {
      var match = this.location.href.replace(/#.*/, '').match(/\?.+/);
      return match ? match[0] : '';
    },

    // Gets the true hash value. Cannot use location.hash directly due to bug
    // in Firefox where location.hash will always be decoded.
    getHash: function(window) {
      var match = (window || this).location.href.match(/#(.*)$/);
      return match ? match[1] : '';
    },

    // Get the pathname and search params, without the root.
    getPath: function() {
      var path = this.decodeFragment(
        this.location.pathname + this.getSearch()
      ).slice(this.root.length - 1);
      return path.charAt(0) === '/' ? path.slice(1) : path;
    },

    // Get the cross-browser normalized URL fragment from the path or hash.
    getFragment: function(fragment) {
      if (fragment == null) {
        if (this._usePushState || !this._wantsHashChange) {
          fragment = this.getPath();
        } else {
          fragment = this.getHash();
        }
      }
      return fragment.replace(routeStripper, '');
    },

    // Start the hash change handling, returning `true` if the current URL matches
    // an existing route, and `false` otherwise.
    start: function(options) {
      if (History.started) throw new Error('Backbone.history has already been started');
      History.started = true;

      // Figure out the initial configuration. Do we need an iframe?
      // Is pushState desired ... is it available?
      this.options          = _.extend({root: '/'}, this.options, options);
      this.root             = this.options.root;
      this._wantsHashChange = this.options.hashChange !== false;
      this._hasHashChange   = 'onhashchange' in window && (document.documentMode === void 0 || document.documentMode > 7);
      this._useHashChange   = this._wantsHashChange && this._hasHashChange;
      this._wantsPushState  = !!this.options.pushState;
      this._hasPushState    = !!(this.history && this.history.pushState);
      this._usePushState    = this._wantsPushState && this._hasPushState;
      this.fragment         = this.getFragment();

      // Normalize root to always include a leading and trailing slash.
      this.root = ('/' + this.root + '/').replace(rootStripper, '/');

      // Transition from hashChange to pushState or vice versa if both are
      // requested.
      if (this._wantsHashChange && this._wantsPushState) {

        // If we've started off with a route from a `pushState`-enabled
        // browser, but we're currently in a browser that doesn't support it...
        if (!this._hasPushState && !this.atRoot()) {
          var rootPath = this.root.slice(0, -1) || '/';
          this.location.replace(rootPath + '#' + this.getPath());
          // Return immediately as browser will do redirect to new url
          return true;

        // Or if we've started out with a hash-based route, but we're currently
        // in a browser where it could be `pushState`-based instead...
        } else if (this._hasPushState && this.atRoot()) {
          this.navigate(this.getHash(), {replace: true});
        }

      }

      // Proxy an iframe to handle location events if the browser doesn't
      // support the `hashchange` event, HTML5 history, or the user wants
      // `hashChange` but not `pushState`.
      if (!this._hasHashChange && this._wantsHashChange && !this._usePushState) {
        this.iframe = document.createElement('iframe');
        this.iframe.src = 'javascript:0';
        this.iframe.style.display = 'none';
        this.iframe.tabIndex = -1;
        var body = document.body;
        // Using `appendChild` will throw on IE < 9 if the document is not ready.
        var iWindow = body.insertBefore(this.iframe, body.firstChild).contentWindow;
        iWindow.document.open();
        iWindow.document.close();
        iWindow.location.hash = '#' + this.fragment;
      }

      // Add a cross-platform `addEventListener` shim for older browsers.
      var addEventListener = window.addEventListener || function(eventName, listener) {
        return attachEvent('on' + eventName, listener);
      };

      // Depending on whether we're using pushState or hashes, and whether
      // 'onhashchange' is supported, determine how we check the URL state.
      if (this._usePushState) {
        addEventListener('popstate', this.checkUrl, false);
      } else if (this._useHashChange && !this.iframe) {
        addEventListener('hashchange', this.checkUrl, false);
      } else if (this._wantsHashChange) {
        this._checkUrlInterval = setInterval(this.checkUrl, this.interval);
      }

      if (!this.options.silent) return this.loadUrl();
    },

    // Disable Backbone.history, perhaps temporarily. Not useful in a real app,
    // but possibly useful for unit testing Routers.
    stop: function() {
      // Add a cross-platform `removeEventListener` shim for older browsers.
      var removeEventListener = window.removeEventListener || function(eventName, listener) {
        return detachEvent('on' + eventName, listener);
      };

      // Remove window listeners.
      if (this._usePushState) {
        removeEventListener('popstate', this.checkUrl, false);
      } else if (this._useHashChange && !this.iframe) {
        removeEventListener('hashchange', this.checkUrl, false);
      }

      // Clean up the iframe if necessary.
      if (this.iframe) {
        document.body.removeChild(this.iframe);
        this.iframe = null;
      }

      // Some environments will throw when clearing an undefined interval.
      if (this._checkUrlInterval) clearInterval(this._checkUrlInterval);
      History.started = false;
    },

    // Add a route to be tested when the fragment changes. Routes added later
    // may override previous routes.
    route: function(route, callback) {
      this.handlers.unshift({route: route, callback: callback});
    },

    // Checks the current URL to see if it has changed, and if it has,
    // calls `loadUrl`, normalizing across the hidden iframe.
    checkUrl: function(e) {
      var current = this.getFragment();

      // If the user pressed the back button, the iframe's hash will have
      // changed and we should use that for comparison.
      if (current === this.fragment && this.iframe) {
        current = this.getHash(this.iframe.contentWindow);
      }

      if (current === this.fragment) return false;
      if (this.iframe) this.navigate(current);
      this.loadUrl();
    },

    // Attempt to load the current URL fragment. If a route succeeds with a
    // match, returns `true`. If no defined routes matches the fragment,
    // returns `false`.
    loadUrl: function(fragment) {
      // If the root doesn't match, no routes can match either.
      if (!this.matchRoot()) return false;
      fragment = this.fragment = this.getFragment(fragment);
      return _.some(this.handlers, function(handler) {
        if (handler.route.test(fragment)) {
          handler.callback(fragment);
          return true;
        }
      });
    },

    // Save a fragment into the hash history, or replace the URL state if the
    // 'replace' option is passed. You are responsible for properly URL-encoding
    // the fragment in advance.
    //
    // The options object can contain `trigger: true` if you wish to have the
    // route callback be fired (not usually desirable), or `replace: true`, if
    // you wish to modify the current URL without adding an entry to the history.
    navigate: function(fragment, options) {
      if (!History.started) return false;
      if (!options || options === true) options = {trigger: !!options};

      // Normalize the fragment.
      fragment = this.getFragment(fragment || '');

      // Don't include a trailing slash on the root.
      var rootPath = this.root;
      if (fragment === '' || fragment.charAt(0) === '?') {
        rootPath = rootPath.slice(0, -1) || '/';
      }
      var url = rootPath + fragment;

      // Strip the fragment of the query and hash for matching.
      fragment = fragment.replace(pathStripper, '');

      // Decode for matching.
      var decodedFragment = this.decodeFragment(fragment);

      if (this.fragment === decodedFragment) return;
      this.fragment = decodedFragment;

      // If pushState is available, we use it to set the fragment as a real URL.
      if (this._usePushState) {
        this.history[options.replace ? 'replaceState' : 'pushState']({}, document.title, url);

      // If hash changes haven't been explicitly disabled, update the hash
      // fragment to store history.
      } else if (this._wantsHashChange) {
        this._updateHash(this.location, fragment, options.replace);
        if (this.iframe && fragment !== this.getHash(this.iframe.contentWindow)) {
          var iWindow = this.iframe.contentWindow;

          // Opening and closing the iframe tricks IE7 and earlier to push a
          // history entry on hash-tag change.  When replace is true, we don't
          // want this.
          if (!options.replace) {
            iWindow.document.open();
            iWindow.document.close();
          }

          this._updateHash(iWindow.location, fragment, options.replace);
        }

      // If you've told us that you explicitly don't want fallback hashchange-
      // based history, then `navigate` becomes a page refresh.
      } else {
        return this.location.assign(url);
      }
      if (options.trigger) return this.loadUrl(fragment);
    },

    // Update the hash location, either replacing the current entry, or adding
    // a new one to the browser history.
    _updateHash: function(location, fragment, replace) {
      if (replace) {
        var href = location.href.replace(/(javascript:|#).*$/, '');
        location.replace(href + '#' + fragment);
      } else {
        // Some browsers require that `hash` contains a leading #.
        location.hash = '#' + fragment;
      }
    }

  });

  // Create the default Backbone.history.
  Backbone.history = new History;

  // Helpers
  // -------

  // Helper function to correctly set up the prototype chain for subclasses.
  // Similar to `goog.inherits`, but uses a hash of prototype properties and
  // class properties to be extended.
  var extend = function(protoProps, staticProps) {
    var parent = this;
    var child;

    // The constructor function for the new subclass is either defined by you
    // (the "constructor" property in your `extend` definition), or defaulted
    // by us to simply call the parent constructor.
    if (protoProps && _.has(protoProps, 'constructor')) {
      child = protoProps.constructor;
    } else {
      child = function(){ return parent.apply(this, arguments); };
    }

    // Add static properties to the constructor function, if supplied.
    _.extend(child, parent, staticProps);

    // Set the prototype chain to inherit from `parent`, without calling
    // `parent`'s constructor function and add the prototype properties.
    child.prototype = _.create(parent.prototype, protoProps);
    child.prototype.constructor = child;

    // Set a convenience property in case the parent's prototype is needed
    // later.
    child.__super__ = parent.prototype;

    return child;
  };

  // Set up inheritance for the model, collection, router, view and history.
  Model.extend = Collection.extend = Router.extend = View.extend = History.extend = extend;

  // Throw an error when a URL is needed, and none is supplied.
  var urlError = function() {
    throw new Error('A "url" property or function must be specified');
  };

  // Wrap an optional error callback with a fallback error event.
  var wrapError = function(model, options) {
    var error = options.error;
    options.error = function(resp) {
      if (error) error.call(options.context, model, resp, options);
      model.trigger('error', model, resp, options);
    };
  };

  return Backbone;
});

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../webpack/buildin/global.js */ "./node_modules/webpack/buildin/global.js")))

/***/ }),

/***/ "./node_modules/bootstrap/js/dist/modal.js":
/*!*************************************************!*\
  !*** ./node_modules/bootstrap/js/dist/modal.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*!
  * Bootstrap modal.js v4.5.0 (https://getbootstrap.com/)
  * Copyright 2011-2020 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
(function (global, factory) {
   true ? module.exports = factory(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), __webpack_require__(/*! ./util.js */ "./node_modules/bootstrap/js/dist/util.js")) :
  undefined;
}(this, (function ($, Util) { 'use strict';

  $ = $ && Object.prototype.hasOwnProperty.call($, 'default') ? $['default'] : $;
  Util = Util && Object.prototype.hasOwnProperty.call(Util, 'default') ? Util['default'] : Util;

  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
  }

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function ownKeys(object, enumerableOnly) {
    var keys = Object.keys(object);

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(object);
      if (enumerableOnly) symbols = symbols.filter(function (sym) {
        return Object.getOwnPropertyDescriptor(object, sym).enumerable;
      });
      keys.push.apply(keys, symbols);
    }

    return keys;
  }

  function _objectSpread2(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};

      if (i % 2) {
        ownKeys(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
      } else {
        ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
    }

    return target;
  }

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  var NAME = 'modal';
  var VERSION = '4.5.0';
  var DATA_KEY = 'bs.modal';
  var EVENT_KEY = "." + DATA_KEY;
  var DATA_API_KEY = '.data-api';
  var JQUERY_NO_CONFLICT = $.fn[NAME];
  var ESCAPE_KEYCODE = 27; // KeyboardEvent.which value for Escape (Esc) key

  var Default = {
    backdrop: true,
    keyboard: true,
    focus: true,
    show: true
  };
  var DefaultType = {
    backdrop: '(boolean|string)',
    keyboard: 'boolean',
    focus: 'boolean',
    show: 'boolean'
  };
  var EVENT_HIDE = "hide" + EVENT_KEY;
  var EVENT_HIDE_PREVENTED = "hidePrevented" + EVENT_KEY;
  var EVENT_HIDDEN = "hidden" + EVENT_KEY;
  var EVENT_SHOW = "show" + EVENT_KEY;
  var EVENT_SHOWN = "shown" + EVENT_KEY;
  var EVENT_FOCUSIN = "focusin" + EVENT_KEY;
  var EVENT_RESIZE = "resize" + EVENT_KEY;
  var EVENT_CLICK_DISMISS = "click.dismiss" + EVENT_KEY;
  var EVENT_KEYDOWN_DISMISS = "keydown.dismiss" + EVENT_KEY;
  var EVENT_MOUSEUP_DISMISS = "mouseup.dismiss" + EVENT_KEY;
  var EVENT_MOUSEDOWN_DISMISS = "mousedown.dismiss" + EVENT_KEY;
  var EVENT_CLICK_DATA_API = "click" + EVENT_KEY + DATA_API_KEY;
  var CLASS_NAME_SCROLLABLE = 'modal-dialog-scrollable';
  var CLASS_NAME_SCROLLBAR_MEASURER = 'modal-scrollbar-measure';
  var CLASS_NAME_BACKDROP = 'modal-backdrop';
  var CLASS_NAME_OPEN = 'modal-open';
  var CLASS_NAME_FADE = 'fade';
  var CLASS_NAME_SHOW = 'show';
  var CLASS_NAME_STATIC = 'modal-static';
  var SELECTOR_DIALOG = '.modal-dialog';
  var SELECTOR_MODAL_BODY = '.modal-body';
  var SELECTOR_DATA_TOGGLE = '[data-toggle="modal"]';
  var SELECTOR_DATA_DISMISS = '[data-dismiss="modal"]';
  var SELECTOR_FIXED_CONTENT = '.fixed-top, .fixed-bottom, .is-fixed, .sticky-top';
  var SELECTOR_STICKY_CONTENT = '.sticky-top';
  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  var Modal = /*#__PURE__*/function () {
    function Modal(element, config) {
      this._config = this._getConfig(config);
      this._element = element;
      this._dialog = element.querySelector(SELECTOR_DIALOG);
      this._backdrop = null;
      this._isShown = false;
      this._isBodyOverflowing = false;
      this._ignoreBackdropClick = false;
      this._isTransitioning = false;
      this._scrollbarWidth = 0;
    } // Getters


    var _proto = Modal.prototype;

    // Public
    _proto.toggle = function toggle(relatedTarget) {
      return this._isShown ? this.hide() : this.show(relatedTarget);
    };

    _proto.show = function show(relatedTarget) {
      var _this = this;

      if (this._isShown || this._isTransitioning) {
        return;
      }

      if ($(this._element).hasClass(CLASS_NAME_FADE)) {
        this._isTransitioning = true;
      }

      var showEvent = $.Event(EVENT_SHOW, {
        relatedTarget: relatedTarget
      });
      $(this._element).trigger(showEvent);

      if (this._isShown || showEvent.isDefaultPrevented()) {
        return;
      }

      this._isShown = true;

      this._checkScrollbar();

      this._setScrollbar();

      this._adjustDialog();

      this._setEscapeEvent();

      this._setResizeEvent();

      $(this._element).on(EVENT_CLICK_DISMISS, SELECTOR_DATA_DISMISS, function (event) {
        return _this.hide(event);
      });
      $(this._dialog).on(EVENT_MOUSEDOWN_DISMISS, function () {
        $(_this._element).one(EVENT_MOUSEUP_DISMISS, function (event) {
          if ($(event.target).is(_this._element)) {
            _this._ignoreBackdropClick = true;
          }
        });
      });

      this._showBackdrop(function () {
        return _this._showElement(relatedTarget);
      });
    };

    _proto.hide = function hide(event) {
      var _this2 = this;

      if (event) {
        event.preventDefault();
      }

      if (!this._isShown || this._isTransitioning) {
        return;
      }

      var hideEvent = $.Event(EVENT_HIDE);
      $(this._element).trigger(hideEvent);

      if (!this._isShown || hideEvent.isDefaultPrevented()) {
        return;
      }

      this._isShown = false;
      var transition = $(this._element).hasClass(CLASS_NAME_FADE);

      if (transition) {
        this._isTransitioning = true;
      }

      this._setEscapeEvent();

      this._setResizeEvent();

      $(document).off(EVENT_FOCUSIN);
      $(this._element).removeClass(CLASS_NAME_SHOW);
      $(this._element).off(EVENT_CLICK_DISMISS);
      $(this._dialog).off(EVENT_MOUSEDOWN_DISMISS);

      if (transition) {
        var transitionDuration = Util.getTransitionDurationFromElement(this._element);
        $(this._element).one(Util.TRANSITION_END, function (event) {
          return _this2._hideModal(event);
        }).emulateTransitionEnd(transitionDuration);
      } else {
        this._hideModal();
      }
    };

    _proto.dispose = function dispose() {
      [window, this._element, this._dialog].forEach(function (htmlElement) {
        return $(htmlElement).off(EVENT_KEY);
      });
      /**
       * `document` has 2 events `EVENT_FOCUSIN` and `EVENT_CLICK_DATA_API`
       * Do not move `document` in `htmlElements` array
       * It will remove `EVENT_CLICK_DATA_API` event that should remain
       */

      $(document).off(EVENT_FOCUSIN);
      $.removeData(this._element, DATA_KEY);
      this._config = null;
      this._element = null;
      this._dialog = null;
      this._backdrop = null;
      this._isShown = null;
      this._isBodyOverflowing = null;
      this._ignoreBackdropClick = null;
      this._isTransitioning = null;
      this._scrollbarWidth = null;
    };

    _proto.handleUpdate = function handleUpdate() {
      this._adjustDialog();
    } // Private
    ;

    _proto._getConfig = function _getConfig(config) {
      config = _objectSpread2(_objectSpread2({}, Default), config);
      Util.typeCheckConfig(NAME, config, DefaultType);
      return config;
    };

    _proto._triggerBackdropTransition = function _triggerBackdropTransition() {
      var _this3 = this;

      if (this._config.backdrop === 'static') {
        var hideEventPrevented = $.Event(EVENT_HIDE_PREVENTED);
        $(this._element).trigger(hideEventPrevented);

        if (hideEventPrevented.defaultPrevented) {
          return;
        }

        this._element.classList.add(CLASS_NAME_STATIC);

        var modalTransitionDuration = Util.getTransitionDurationFromElement(this._element);
        $(this._element).one(Util.TRANSITION_END, function () {
          _this3._element.classList.remove(CLASS_NAME_STATIC);
        }).emulateTransitionEnd(modalTransitionDuration);

        this._element.focus();
      } else {
        this.hide();
      }
    };

    _proto._showElement = function _showElement(relatedTarget) {
      var _this4 = this;

      var transition = $(this._element).hasClass(CLASS_NAME_FADE);
      var modalBody = this._dialog ? this._dialog.querySelector(SELECTOR_MODAL_BODY) : null;

      if (!this._element.parentNode || this._element.parentNode.nodeType !== Node.ELEMENT_NODE) {
        // Don't move modal's DOM position
        document.body.appendChild(this._element);
      }

      this._element.style.display = 'block';

      this._element.removeAttribute('aria-hidden');

      this._element.setAttribute('aria-modal', true);

      if ($(this._dialog).hasClass(CLASS_NAME_SCROLLABLE) && modalBody) {
        modalBody.scrollTop = 0;
      } else {
        this._element.scrollTop = 0;
      }

      if (transition) {
        Util.reflow(this._element);
      }

      $(this._element).addClass(CLASS_NAME_SHOW);

      if (this._config.focus) {
        this._enforceFocus();
      }

      var shownEvent = $.Event(EVENT_SHOWN, {
        relatedTarget: relatedTarget
      });

      var transitionComplete = function transitionComplete() {
        if (_this4._config.focus) {
          _this4._element.focus();
        }

        _this4._isTransitioning = false;
        $(_this4._element).trigger(shownEvent);
      };

      if (transition) {
        var transitionDuration = Util.getTransitionDurationFromElement(this._dialog);
        $(this._dialog).one(Util.TRANSITION_END, transitionComplete).emulateTransitionEnd(transitionDuration);
      } else {
        transitionComplete();
      }
    };

    _proto._enforceFocus = function _enforceFocus() {
      var _this5 = this;

      $(document).off(EVENT_FOCUSIN) // Guard against infinite focus loop
      .on(EVENT_FOCUSIN, function (event) {
        if (document !== event.target && _this5._element !== event.target && $(_this5._element).has(event.target).length === 0) {
          _this5._element.focus();
        }
      });
    };

    _proto._setEscapeEvent = function _setEscapeEvent() {
      var _this6 = this;

      if (this._isShown) {
        $(this._element).on(EVENT_KEYDOWN_DISMISS, function (event) {
          if (_this6._config.keyboard && event.which === ESCAPE_KEYCODE) {
            event.preventDefault();

            _this6.hide();
          } else if (!_this6._config.keyboard && event.which === ESCAPE_KEYCODE) {
            _this6._triggerBackdropTransition();
          }
        });
      } else if (!this._isShown) {
        $(this._element).off(EVENT_KEYDOWN_DISMISS);
      }
    };

    _proto._setResizeEvent = function _setResizeEvent() {
      var _this7 = this;

      if (this._isShown) {
        $(window).on(EVENT_RESIZE, function (event) {
          return _this7.handleUpdate(event);
        });
      } else {
        $(window).off(EVENT_RESIZE);
      }
    };

    _proto._hideModal = function _hideModal() {
      var _this8 = this;

      this._element.style.display = 'none';

      this._element.setAttribute('aria-hidden', true);

      this._element.removeAttribute('aria-modal');

      this._isTransitioning = false;

      this._showBackdrop(function () {
        $(document.body).removeClass(CLASS_NAME_OPEN);

        _this8._resetAdjustments();

        _this8._resetScrollbar();

        $(_this8._element).trigger(EVENT_HIDDEN);
      });
    };

    _proto._removeBackdrop = function _removeBackdrop() {
      if (this._backdrop) {
        $(this._backdrop).remove();
        this._backdrop = null;
      }
    };

    _proto._showBackdrop = function _showBackdrop(callback) {
      var _this9 = this;

      var animate = $(this._element).hasClass(CLASS_NAME_FADE) ? CLASS_NAME_FADE : '';

      if (this._isShown && this._config.backdrop) {
        this._backdrop = document.createElement('div');
        this._backdrop.className = CLASS_NAME_BACKDROP;

        if (animate) {
          this._backdrop.classList.add(animate);
        }

        $(this._backdrop).appendTo(document.body);
        $(this._element).on(EVENT_CLICK_DISMISS, function (event) {
          if (_this9._ignoreBackdropClick) {
            _this9._ignoreBackdropClick = false;
            return;
          }

          if (event.target !== event.currentTarget) {
            return;
          }

          _this9._triggerBackdropTransition();
        });

        if (animate) {
          Util.reflow(this._backdrop);
        }

        $(this._backdrop).addClass(CLASS_NAME_SHOW);

        if (!callback) {
          return;
        }

        if (!animate) {
          callback();
          return;
        }

        var backdropTransitionDuration = Util.getTransitionDurationFromElement(this._backdrop);
        $(this._backdrop).one(Util.TRANSITION_END, callback).emulateTransitionEnd(backdropTransitionDuration);
      } else if (!this._isShown && this._backdrop) {
        $(this._backdrop).removeClass(CLASS_NAME_SHOW);

        var callbackRemove = function callbackRemove() {
          _this9._removeBackdrop();

          if (callback) {
            callback();
          }
        };

        if ($(this._element).hasClass(CLASS_NAME_FADE)) {
          var _backdropTransitionDuration = Util.getTransitionDurationFromElement(this._backdrop);

          $(this._backdrop).one(Util.TRANSITION_END, callbackRemove).emulateTransitionEnd(_backdropTransitionDuration);
        } else {
          callbackRemove();
        }
      } else if (callback) {
        callback();
      }
    } // ----------------------------------------------------------------------
    // the following methods are used to handle overflowing modals
    // todo (fat): these should probably be refactored out of modal.js
    // ----------------------------------------------------------------------
    ;

    _proto._adjustDialog = function _adjustDialog() {
      var isModalOverflowing = this._element.scrollHeight > document.documentElement.clientHeight;

      if (!this._isBodyOverflowing && isModalOverflowing) {
        this._element.style.paddingLeft = this._scrollbarWidth + "px";
      }

      if (this._isBodyOverflowing && !isModalOverflowing) {
        this._element.style.paddingRight = this._scrollbarWidth + "px";
      }
    };

    _proto._resetAdjustments = function _resetAdjustments() {
      this._element.style.paddingLeft = '';
      this._element.style.paddingRight = '';
    };

    _proto._checkScrollbar = function _checkScrollbar() {
      var rect = document.body.getBoundingClientRect();
      this._isBodyOverflowing = Math.round(rect.left + rect.right) < window.innerWidth;
      this._scrollbarWidth = this._getScrollbarWidth();
    };

    _proto._setScrollbar = function _setScrollbar() {
      var _this10 = this;

      if (this._isBodyOverflowing) {
        // Note: DOMNode.style.paddingRight returns the actual value or '' if not set
        //   while $(DOMNode).css('padding-right') returns the calculated value or 0 if not set
        var fixedContent = [].slice.call(document.querySelectorAll(SELECTOR_FIXED_CONTENT));
        var stickyContent = [].slice.call(document.querySelectorAll(SELECTOR_STICKY_CONTENT)); // Adjust fixed content padding

        $(fixedContent).each(function (index, element) {
          var actualPadding = element.style.paddingRight;
          var calculatedPadding = $(element).css('padding-right');
          $(element).data('padding-right', actualPadding).css('padding-right', parseFloat(calculatedPadding) + _this10._scrollbarWidth + "px");
        }); // Adjust sticky content margin

        $(stickyContent).each(function (index, element) {
          var actualMargin = element.style.marginRight;
          var calculatedMargin = $(element).css('margin-right');
          $(element).data('margin-right', actualMargin).css('margin-right', parseFloat(calculatedMargin) - _this10._scrollbarWidth + "px");
        }); // Adjust body padding

        var actualPadding = document.body.style.paddingRight;
        var calculatedPadding = $(document.body).css('padding-right');
        $(document.body).data('padding-right', actualPadding).css('padding-right', parseFloat(calculatedPadding) + this._scrollbarWidth + "px");
      }

      $(document.body).addClass(CLASS_NAME_OPEN);
    };

    _proto._resetScrollbar = function _resetScrollbar() {
      // Restore fixed content padding
      var fixedContent = [].slice.call(document.querySelectorAll(SELECTOR_FIXED_CONTENT));
      $(fixedContent).each(function (index, element) {
        var padding = $(element).data('padding-right');
        $(element).removeData('padding-right');
        element.style.paddingRight = padding ? padding : '';
      }); // Restore sticky content

      var elements = [].slice.call(document.querySelectorAll("" + SELECTOR_STICKY_CONTENT));
      $(elements).each(function (index, element) {
        var margin = $(element).data('margin-right');

        if (typeof margin !== 'undefined') {
          $(element).css('margin-right', margin).removeData('margin-right');
        }
      }); // Restore body padding

      var padding = $(document.body).data('padding-right');
      $(document.body).removeData('padding-right');
      document.body.style.paddingRight = padding ? padding : '';
    };

    _proto._getScrollbarWidth = function _getScrollbarWidth() {
      // thx d.walsh
      var scrollDiv = document.createElement('div');
      scrollDiv.className = CLASS_NAME_SCROLLBAR_MEASURER;
      document.body.appendChild(scrollDiv);
      var scrollbarWidth = scrollDiv.getBoundingClientRect().width - scrollDiv.clientWidth;
      document.body.removeChild(scrollDiv);
      return scrollbarWidth;
    } // Static
    ;

    Modal._jQueryInterface = function _jQueryInterface(config, relatedTarget) {
      return this.each(function () {
        var data = $(this).data(DATA_KEY);

        var _config = _objectSpread2(_objectSpread2(_objectSpread2({}, Default), $(this).data()), typeof config === 'object' && config ? config : {});

        if (!data) {
          data = new Modal(this, _config);
          $(this).data(DATA_KEY, data);
        }

        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError("No method named \"" + config + "\"");
          }

          data[config](relatedTarget);
        } else if (_config.show) {
          data.show(relatedTarget);
        }
      });
    };

    _createClass(Modal, null, [{
      key: "VERSION",
      get: function get() {
        return VERSION;
      }
    }, {
      key: "Default",
      get: function get() {
        return Default;
      }
    }]);

    return Modal;
  }();
  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */


  $(document).on(EVENT_CLICK_DATA_API, SELECTOR_DATA_TOGGLE, function (event) {
    var _this11 = this;

    var target;
    var selector = Util.getSelectorFromElement(this);

    if (selector) {
      target = document.querySelector(selector);
    }

    var config = $(target).data(DATA_KEY) ? 'toggle' : _objectSpread2(_objectSpread2({}, $(target).data()), $(this).data());

    if (this.tagName === 'A' || this.tagName === 'AREA') {
      event.preventDefault();
    }

    var $target = $(target).one(EVENT_SHOW, function (showEvent) {
      if (showEvent.isDefaultPrevented()) {
        // Only register focus restorer if modal will actually get shown
        return;
      }

      $target.one(EVENT_HIDDEN, function () {
        if ($(_this11).is(':visible')) {
          _this11.focus();
        }
      });
    });

    Modal._jQueryInterface.call($(target), config, this);
  });
  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME] = Modal._jQueryInterface;
  $.fn[NAME].Constructor = Modal;

  $.fn[NAME].noConflict = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT;
    return Modal._jQueryInterface;
  };

  return Modal;

})));
//# sourceMappingURL=modal.js.map


/***/ }),

/***/ "./node_modules/bootstrap/js/dist/tab.js":
/*!***********************************************!*\
  !*** ./node_modules/bootstrap/js/dist/tab.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*!
  * Bootstrap tab.js v4.5.0 (https://getbootstrap.com/)
  * Copyright 2011-2020 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
(function (global, factory) {
   true ? module.exports = factory(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), __webpack_require__(/*! ./util.js */ "./node_modules/bootstrap/js/dist/util.js")) :
  undefined;
}(this, (function ($, Util) { 'use strict';

  $ = $ && Object.prototype.hasOwnProperty.call($, 'default') ? $['default'] : $;
  Util = Util && Object.prototype.hasOwnProperty.call(Util, 'default') ? Util['default'] : Util;

  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
  }

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  var NAME = 'tab';
  var VERSION = '4.5.0';
  var DATA_KEY = 'bs.tab';
  var EVENT_KEY = "." + DATA_KEY;
  var DATA_API_KEY = '.data-api';
  var JQUERY_NO_CONFLICT = $.fn[NAME];
  var EVENT_HIDE = "hide" + EVENT_KEY;
  var EVENT_HIDDEN = "hidden" + EVENT_KEY;
  var EVENT_SHOW = "show" + EVENT_KEY;
  var EVENT_SHOWN = "shown" + EVENT_KEY;
  var EVENT_CLICK_DATA_API = "click" + EVENT_KEY + DATA_API_KEY;
  var CLASS_NAME_DROPDOWN_MENU = 'dropdown-menu';
  var CLASS_NAME_ACTIVE = 'active';
  var CLASS_NAME_DISABLED = 'disabled';
  var CLASS_NAME_FADE = 'fade';
  var CLASS_NAME_SHOW = 'show';
  var SELECTOR_DROPDOWN = '.dropdown';
  var SELECTOR_NAV_LIST_GROUP = '.nav, .list-group';
  var SELECTOR_ACTIVE = '.active';
  var SELECTOR_ACTIVE_UL = '> li > .active';
  var SELECTOR_DATA_TOGGLE = '[data-toggle="tab"], [data-toggle="pill"], [data-toggle="list"]';
  var SELECTOR_DROPDOWN_TOGGLE = '.dropdown-toggle';
  var SELECTOR_DROPDOWN_ACTIVE_CHILD = '> .dropdown-menu .active';
  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  var Tab = /*#__PURE__*/function () {
    function Tab(element) {
      this._element = element;
    } // Getters


    var _proto = Tab.prototype;

    // Public
    _proto.show = function show() {
      var _this = this;

      if (this._element.parentNode && this._element.parentNode.nodeType === Node.ELEMENT_NODE && $(this._element).hasClass(CLASS_NAME_ACTIVE) || $(this._element).hasClass(CLASS_NAME_DISABLED)) {
        return;
      }

      var target;
      var previous;
      var listElement = $(this._element).closest(SELECTOR_NAV_LIST_GROUP)[0];
      var selector = Util.getSelectorFromElement(this._element);

      if (listElement) {
        var itemSelector = listElement.nodeName === 'UL' || listElement.nodeName === 'OL' ? SELECTOR_ACTIVE_UL : SELECTOR_ACTIVE;
        previous = $.makeArray($(listElement).find(itemSelector));
        previous = previous[previous.length - 1];
      }

      var hideEvent = $.Event(EVENT_HIDE, {
        relatedTarget: this._element
      });
      var showEvent = $.Event(EVENT_SHOW, {
        relatedTarget: previous
      });

      if (previous) {
        $(previous).trigger(hideEvent);
      }

      $(this._element).trigger(showEvent);

      if (showEvent.isDefaultPrevented() || hideEvent.isDefaultPrevented()) {
        return;
      }

      if (selector) {
        target = document.querySelector(selector);
      }

      this._activate(this._element, listElement);

      var complete = function complete() {
        var hiddenEvent = $.Event(EVENT_HIDDEN, {
          relatedTarget: _this._element
        });
        var shownEvent = $.Event(EVENT_SHOWN, {
          relatedTarget: previous
        });
        $(previous).trigger(hiddenEvent);
        $(_this._element).trigger(shownEvent);
      };

      if (target) {
        this._activate(target, target.parentNode, complete);
      } else {
        complete();
      }
    };

    _proto.dispose = function dispose() {
      $.removeData(this._element, DATA_KEY);
      this._element = null;
    } // Private
    ;

    _proto._activate = function _activate(element, container, callback) {
      var _this2 = this;

      var activeElements = container && (container.nodeName === 'UL' || container.nodeName === 'OL') ? $(container).find(SELECTOR_ACTIVE_UL) : $(container).children(SELECTOR_ACTIVE);
      var active = activeElements[0];
      var isTransitioning = callback && active && $(active).hasClass(CLASS_NAME_FADE);

      var complete = function complete() {
        return _this2._transitionComplete(element, active, callback);
      };

      if (active && isTransitioning) {
        var transitionDuration = Util.getTransitionDurationFromElement(active);
        $(active).removeClass(CLASS_NAME_SHOW).one(Util.TRANSITION_END, complete).emulateTransitionEnd(transitionDuration);
      } else {
        complete();
      }
    };

    _proto._transitionComplete = function _transitionComplete(element, active, callback) {
      if (active) {
        $(active).removeClass(CLASS_NAME_ACTIVE);
        var dropdownChild = $(active.parentNode).find(SELECTOR_DROPDOWN_ACTIVE_CHILD)[0];

        if (dropdownChild) {
          $(dropdownChild).removeClass(CLASS_NAME_ACTIVE);
        }

        if (active.getAttribute('role') === 'tab') {
          active.setAttribute('aria-selected', false);
        }
      }

      $(element).addClass(CLASS_NAME_ACTIVE);

      if (element.getAttribute('role') === 'tab') {
        element.setAttribute('aria-selected', true);
      }

      Util.reflow(element);

      if (element.classList.contains(CLASS_NAME_FADE)) {
        element.classList.add(CLASS_NAME_SHOW);
      }

      if (element.parentNode && $(element.parentNode).hasClass(CLASS_NAME_DROPDOWN_MENU)) {
        var dropdownElement = $(element).closest(SELECTOR_DROPDOWN)[0];

        if (dropdownElement) {
          var dropdownToggleList = [].slice.call(dropdownElement.querySelectorAll(SELECTOR_DROPDOWN_TOGGLE));
          $(dropdownToggleList).addClass(CLASS_NAME_ACTIVE);
        }

        element.setAttribute('aria-expanded', true);
      }

      if (callback) {
        callback();
      }
    } // Static
    ;

    Tab._jQueryInterface = function _jQueryInterface(config) {
      return this.each(function () {
        var $this = $(this);
        var data = $this.data(DATA_KEY);

        if (!data) {
          data = new Tab(this);
          $this.data(DATA_KEY, data);
        }

        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError("No method named \"" + config + "\"");
          }

          data[config]();
        }
      });
    };

    _createClass(Tab, null, [{
      key: "VERSION",
      get: function get() {
        return VERSION;
      }
    }]);

    return Tab;
  }();
  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */


  $(document).on(EVENT_CLICK_DATA_API, SELECTOR_DATA_TOGGLE, function (event) {
    event.preventDefault();

    Tab._jQueryInterface.call($(this), 'show');
  });
  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */

  $.fn[NAME] = Tab._jQueryInterface;
  $.fn[NAME].Constructor = Tab;

  $.fn[NAME].noConflict = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT;
    return Tab._jQueryInterface;
  };

  return Tab;

})));
//# sourceMappingURL=tab.js.map


/***/ }),

/***/ "./node_modules/bootstrap/js/dist/toast.js":
/*!*************************************************!*\
  !*** ./node_modules/bootstrap/js/dist/toast.js ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*!
  * Bootstrap toast.js v4.5.0 (https://getbootstrap.com/)
  * Copyright 2011-2020 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
(function (global, factory) {
   true ? module.exports = factory(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"), __webpack_require__(/*! ./util.js */ "./node_modules/bootstrap/js/dist/util.js")) :
  undefined;
}(this, (function ($, Util) { 'use strict';

  $ = $ && Object.prototype.hasOwnProperty.call($, 'default') ? $['default'] : $;
  Util = Util && Object.prototype.hasOwnProperty.call(Util, 'default') ? Util['default'] : Util;

  function _defineProperties(target, props) {
    for (var i = 0; i < props.length; i++) {
      var descriptor = props[i];
      descriptor.enumerable = descriptor.enumerable || false;
      descriptor.configurable = true;
      if ("value" in descriptor) descriptor.writable = true;
      Object.defineProperty(target, descriptor.key, descriptor);
    }
  }

  function _createClass(Constructor, protoProps, staticProps) {
    if (protoProps) _defineProperties(Constructor.prototype, protoProps);
    if (staticProps) _defineProperties(Constructor, staticProps);
    return Constructor;
  }

  function _defineProperty(obj, key, value) {
    if (key in obj) {
      Object.defineProperty(obj, key, {
        value: value,
        enumerable: true,
        configurable: true,
        writable: true
      });
    } else {
      obj[key] = value;
    }

    return obj;
  }

  function ownKeys(object, enumerableOnly) {
    var keys = Object.keys(object);

    if (Object.getOwnPropertySymbols) {
      var symbols = Object.getOwnPropertySymbols(object);
      if (enumerableOnly) symbols = symbols.filter(function (sym) {
        return Object.getOwnPropertyDescriptor(object, sym).enumerable;
      });
      keys.push.apply(keys, symbols);
    }

    return keys;
  }

  function _objectSpread2(target) {
    for (var i = 1; i < arguments.length; i++) {
      var source = arguments[i] != null ? arguments[i] : {};

      if (i % 2) {
        ownKeys(Object(source), true).forEach(function (key) {
          _defineProperty(target, key, source[key]);
        });
      } else if (Object.getOwnPropertyDescriptors) {
        Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));
      } else {
        ownKeys(Object(source)).forEach(function (key) {
          Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));
        });
      }
    }

    return target;
  }

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  var NAME = 'toast';
  var VERSION = '4.5.0';
  var DATA_KEY = 'bs.toast';
  var EVENT_KEY = "." + DATA_KEY;
  var JQUERY_NO_CONFLICT = $.fn[NAME];
  var EVENT_CLICK_DISMISS = "click.dismiss" + EVENT_KEY;
  var EVENT_HIDE = "hide" + EVENT_KEY;
  var EVENT_HIDDEN = "hidden" + EVENT_KEY;
  var EVENT_SHOW = "show" + EVENT_KEY;
  var EVENT_SHOWN = "shown" + EVENT_KEY;
  var CLASS_NAME_FADE = 'fade';
  var CLASS_NAME_HIDE = 'hide';
  var CLASS_NAME_SHOW = 'show';
  var CLASS_NAME_SHOWING = 'showing';
  var DefaultType = {
    animation: 'boolean',
    autohide: 'boolean',
    delay: 'number'
  };
  var Default = {
    animation: true,
    autohide: true,
    delay: 500
  };
  var SELECTOR_DATA_DISMISS = '[data-dismiss="toast"]';
  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  var Toast = /*#__PURE__*/function () {
    function Toast(element, config) {
      this._element = element;
      this._config = this._getConfig(config);
      this._timeout = null;

      this._setListeners();
    } // Getters


    var _proto = Toast.prototype;

    // Public
    _proto.show = function show() {
      var _this = this;

      var showEvent = $.Event(EVENT_SHOW);
      $(this._element).trigger(showEvent);

      if (showEvent.isDefaultPrevented()) {
        return;
      }

      if (this._config.animation) {
        this._element.classList.add(CLASS_NAME_FADE);
      }

      var complete = function complete() {
        _this._element.classList.remove(CLASS_NAME_SHOWING);

        _this._element.classList.add(CLASS_NAME_SHOW);

        $(_this._element).trigger(EVENT_SHOWN);

        if (_this._config.autohide) {
          _this._timeout = setTimeout(function () {
            _this.hide();
          }, _this._config.delay);
        }
      };

      this._element.classList.remove(CLASS_NAME_HIDE);

      Util.reflow(this._element);

      this._element.classList.add(CLASS_NAME_SHOWING);

      if (this._config.animation) {
        var transitionDuration = Util.getTransitionDurationFromElement(this._element);
        $(this._element).one(Util.TRANSITION_END, complete).emulateTransitionEnd(transitionDuration);
      } else {
        complete();
      }
    };

    _proto.hide = function hide() {
      if (!this._element.classList.contains(CLASS_NAME_SHOW)) {
        return;
      }

      var hideEvent = $.Event(EVENT_HIDE);
      $(this._element).trigger(hideEvent);

      if (hideEvent.isDefaultPrevented()) {
        return;
      }

      this._close();
    };

    _proto.dispose = function dispose() {
      clearTimeout(this._timeout);
      this._timeout = null;

      if (this._element.classList.contains(CLASS_NAME_SHOW)) {
        this._element.classList.remove(CLASS_NAME_SHOW);
      }

      $(this._element).off(EVENT_CLICK_DISMISS);
      $.removeData(this._element, DATA_KEY);
      this._element = null;
      this._config = null;
    } // Private
    ;

    _proto._getConfig = function _getConfig(config) {
      config = _objectSpread2(_objectSpread2(_objectSpread2({}, Default), $(this._element).data()), typeof config === 'object' && config ? config : {});
      Util.typeCheckConfig(NAME, config, this.constructor.DefaultType);
      return config;
    };

    _proto._setListeners = function _setListeners() {
      var _this2 = this;

      $(this._element).on(EVENT_CLICK_DISMISS, SELECTOR_DATA_DISMISS, function () {
        return _this2.hide();
      });
    };

    _proto._close = function _close() {
      var _this3 = this;

      var complete = function complete() {
        _this3._element.classList.add(CLASS_NAME_HIDE);

        $(_this3._element).trigger(EVENT_HIDDEN);
      };

      this._element.classList.remove(CLASS_NAME_SHOW);

      if (this._config.animation) {
        var transitionDuration = Util.getTransitionDurationFromElement(this._element);
        $(this._element).one(Util.TRANSITION_END, complete).emulateTransitionEnd(transitionDuration);
      } else {
        complete();
      }
    } // Static
    ;

    Toast._jQueryInterface = function _jQueryInterface(config) {
      return this.each(function () {
        var $element = $(this);
        var data = $element.data(DATA_KEY);

        var _config = typeof config === 'object' && config;

        if (!data) {
          data = new Toast(this, _config);
          $element.data(DATA_KEY, data);
        }

        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError("No method named \"" + config + "\"");
          }

          data[config](this);
        }
      });
    };

    _createClass(Toast, null, [{
      key: "VERSION",
      get: function get() {
        return VERSION;
      }
    }, {
      key: "DefaultType",
      get: function get() {
        return DefaultType;
      }
    }, {
      key: "Default",
      get: function get() {
        return Default;
      }
    }]);

    return Toast;
  }();
  /**
   * ------------------------------------------------------------------------
   * jQuery
   * ------------------------------------------------------------------------
   */


  $.fn[NAME] = Toast._jQueryInterface;
  $.fn[NAME].Constructor = Toast;

  $.fn[NAME].noConflict = function () {
    $.fn[NAME] = JQUERY_NO_CONFLICT;
    return Toast._jQueryInterface;
  };

  return Toast;

})));
//# sourceMappingURL=toast.js.map


/***/ }),

/***/ "./node_modules/bootstrap/js/dist/util.js":
/*!************************************************!*\
  !*** ./node_modules/bootstrap/js/dist/util.js ***!
  \************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*!
  * Bootstrap util.js v4.5.0 (https://getbootstrap.com/)
  * Copyright 2011-2020 The Bootstrap Authors (https://github.com/twbs/bootstrap/graphs/contributors)
  * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
  */
(function (global, factory) {
   true ? module.exports = factory(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")) :
  undefined;
}(this, (function ($) { 'use strict';

  $ = $ && Object.prototype.hasOwnProperty.call($, 'default') ? $['default'] : $;

  /**
   * --------------------------------------------------------------------------
   * Bootstrap (v4.5.0): util.js
   * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
   * --------------------------------------------------------------------------
   */
  /**
   * ------------------------------------------------------------------------
   * Private TransitionEnd Helpers
   * ------------------------------------------------------------------------
   */

  var TRANSITION_END = 'transitionend';
  var MAX_UID = 1000000;
  var MILLISECONDS_MULTIPLIER = 1000; // Shoutout AngusCroll (https://goo.gl/pxwQGp)

  function toType(obj) {
    if (obj === null || typeof obj === 'undefined') {
      return "" + obj;
    }

    return {}.toString.call(obj).match(/\s([a-z]+)/i)[1].toLowerCase();
  }

  function getSpecialTransitionEndEvent() {
    return {
      bindType: TRANSITION_END,
      delegateType: TRANSITION_END,
      handle: function handle(event) {
        if ($(event.target).is(this)) {
          return event.handleObj.handler.apply(this, arguments); // eslint-disable-line prefer-rest-params
        }

        return undefined;
      }
    };
  }

  function transitionEndEmulator(duration) {
    var _this = this;

    var called = false;
    $(this).one(Util.TRANSITION_END, function () {
      called = true;
    });
    setTimeout(function () {
      if (!called) {
        Util.triggerTransitionEnd(_this);
      }
    }, duration);
    return this;
  }

  function setTransitionEndSupport() {
    $.fn.emulateTransitionEnd = transitionEndEmulator;
    $.event.special[Util.TRANSITION_END] = getSpecialTransitionEndEvent();
  }
  /**
   * --------------------------------------------------------------------------
   * Public Util Api
   * --------------------------------------------------------------------------
   */


  var Util = {
    TRANSITION_END: 'bsTransitionEnd',
    getUID: function getUID(prefix) {
      do {
        // eslint-disable-next-line no-bitwise
        prefix += ~~(Math.random() * MAX_UID); // "~~" acts like a faster Math.floor() here
      } while (document.getElementById(prefix));

      return prefix;
    },
    getSelectorFromElement: function getSelectorFromElement(element) {
      var selector = element.getAttribute('data-target');

      if (!selector || selector === '#') {
        var hrefAttr = element.getAttribute('href');
        selector = hrefAttr && hrefAttr !== '#' ? hrefAttr.trim() : '';
      }

      try {
        return document.querySelector(selector) ? selector : null;
      } catch (err) {
        return null;
      }
    },
    getTransitionDurationFromElement: function getTransitionDurationFromElement(element) {
      if (!element) {
        return 0;
      } // Get transition-duration of the element


      var transitionDuration = $(element).css('transition-duration');
      var transitionDelay = $(element).css('transition-delay');
      var floatTransitionDuration = parseFloat(transitionDuration);
      var floatTransitionDelay = parseFloat(transitionDelay); // Return 0 if element or transition duration is not found

      if (!floatTransitionDuration && !floatTransitionDelay) {
        return 0;
      } // If multiple durations are defined, take the first


      transitionDuration = transitionDuration.split(',')[0];
      transitionDelay = transitionDelay.split(',')[0];
      return (parseFloat(transitionDuration) + parseFloat(transitionDelay)) * MILLISECONDS_MULTIPLIER;
    },
    reflow: function reflow(element) {
      return element.offsetHeight;
    },
    triggerTransitionEnd: function triggerTransitionEnd(element) {
      $(element).trigger(TRANSITION_END);
    },
    // TODO: Remove in v5
    supportsTransitionEnd: function supportsTransitionEnd() {
      return Boolean(TRANSITION_END);
    },
    isElement: function isElement(obj) {
      return (obj[0] || obj).nodeType;
    },
    typeCheckConfig: function typeCheckConfig(componentName, config, configTypes) {
      for (var property in configTypes) {
        if (Object.prototype.hasOwnProperty.call(configTypes, property)) {
          var expectedTypes = configTypes[property];
          var value = config[property];
          var valueType = value && Util.isElement(value) ? 'element' : toType(value);

          if (!new RegExp(expectedTypes).test(valueType)) {
            throw new Error(componentName.toUpperCase() + ": " + ("Option \"" + property + "\" provided type \"" + valueType + "\" ") + ("but expected type \"" + expectedTypes + "\"."));
          }
        }
      }
    },
    findShadowRoot: function findShadowRoot(element) {
      if (!document.documentElement.attachShadow) {
        return null;
      } // Can find the shadow root otherwise it'll return the document


      if (typeof element.getRootNode === 'function') {
        var root = element.getRootNode();
        return root instanceof ShadowRoot ? root : null;
      }

      if (element instanceof ShadowRoot) {
        return element;
      } // when we don't find a shadow root


      if (!element.parentNode) {
        return null;
      }

      return Util.findShadowRoot(element.parentNode);
    },
    jQueryDetection: function jQueryDetection() {
      if (typeof $ === 'undefined') {
        throw new TypeError('Bootstrap\'s JavaScript requires jQuery. jQuery must be included before Bootstrap\'s JavaScript.');
      }

      var version = $.fn.jquery.split(' ')[0].split('.');
      var minMajor = 1;
      var ltMajor = 2;
      var minMinor = 9;
      var minPatch = 1;
      var maxMajor = 4;

      if (version[0] < ltMajor && version[1] < minMinor || version[0] === minMajor && version[1] === minMinor && version[2] < minPatch || version[0] >= maxMajor) {
        throw new Error('Bootstrap\'s JavaScript requires at least jQuery v1.9.1 but less than v4.0.0');
      }
    }
  };
  Util.jQueryDetection();
  setTransitionEndSupport();

  return Util;

})));
//# sourceMappingURL=util.js.map


/***/ }),

/***/ "./node_modules/ev-emitter/ev-emitter.js":
/*!***********************************************!*\
  !*** ./node_modules/ev-emitter/ev-emitter.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_RESULT__;/**
 * EvEmitter v1.1.0
 * Lil' event emitter
 * MIT License
 */

/* jshint unused: true, undef: true, strict: true */

( function( global, factory ) {
  // universal module definition
  /* jshint strict: false */ /* globals define, module, window */
  if ( true ) {
    // AMD - RequireJS
    !(__WEBPACK_AMD_DEFINE_FACTORY__ = (factory),
				__WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ?
				(__WEBPACK_AMD_DEFINE_FACTORY__.call(exports, __webpack_require__, exports, module)) :
				__WEBPACK_AMD_DEFINE_FACTORY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
  } else {}

}( typeof window != 'undefined' ? window : this, function() {

"use strict";

function EvEmitter() {}

var proto = EvEmitter.prototype;

proto.on = function( eventName, listener ) {
  if ( !eventName || !listener ) {
    return;
  }
  // set events hash
  var events = this._events = this._events || {};
  // set listeners array
  var listeners = events[ eventName ] = events[ eventName ] || [];
  // only add once
  if ( listeners.indexOf( listener ) == -1 ) {
    listeners.push( listener );
  }

  return this;
};

proto.once = function( eventName, listener ) {
  if ( !eventName || !listener ) {
    return;
  }
  // add event
  this.on( eventName, listener );
  // set once flag
  // set onceEvents hash
  var onceEvents = this._onceEvents = this._onceEvents || {};
  // set onceListeners object
  var onceListeners = onceEvents[ eventName ] = onceEvents[ eventName ] || {};
  // set flag
  onceListeners[ listener ] = true;

  return this;
};

proto.off = function( eventName, listener ) {
  var listeners = this._events && this._events[ eventName ];
  if ( !listeners || !listeners.length ) {
    return;
  }
  var index = listeners.indexOf( listener );
  if ( index != -1 ) {
    listeners.splice( index, 1 );
  }

  return this;
};

proto.emitEvent = function( eventName, args ) {
  var listeners = this._events && this._events[ eventName ];
  if ( !listeners || !listeners.length ) {
    return;
  }
  // copy over to avoid interference if .off() in listener
  listeners = listeners.slice(0);
  args = args || [];
  // once stuff
  var onceListeners = this._onceEvents && this._onceEvents[ eventName ];

  for ( var i=0; i < listeners.length; i++ ) {
    var listener = listeners[i]
    var isOnce = onceListeners && onceListeners[ listener ];
    if ( isOnce ) {
      // remove listener
      // remove before trigger to prevent recursion
      this.off( eventName, listener );
      // unset once flag
      delete onceListeners[ listener ];
    }
    // trigger listener
    listener.apply( this, args );
  }

  return this;
};

proto.allOff = function() {
  delete this._events;
  delete this._onceEvents;
};

return EvEmitter;

}));


/***/ }),

/***/ "./node_modules/imagesloaded/imagesloaded.js":
/*!***************************************************!*\
  !*** ./node_modules/imagesloaded/imagesloaded.js ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
 * imagesLoaded v4.1.4
 * JavaScript is all like "You images are done yet or what?"
 * MIT License
 */

( function( window, factory ) { 'use strict';
  // universal module definition

  /*global define: false, module: false, require: false */

  if ( true ) {
    // AMD
    !(__WEBPACK_AMD_DEFINE_ARRAY__ = [
      __webpack_require__(/*! ev-emitter/ev-emitter */ "./node_modules/ev-emitter/ev-emitter.js")
    ], __WEBPACK_AMD_DEFINE_RESULT__ = (function( EvEmitter ) {
      return factory( window, EvEmitter );
    }).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
  } else {}

})( typeof window !== 'undefined' ? window : this,

// --------------------------  factory -------------------------- //

function factory( window, EvEmitter ) {

'use strict';

var $ = window.jQuery;
var console = window.console;

// -------------------------- helpers -------------------------- //

// extend objects
function extend( a, b ) {
  for ( var prop in b ) {
    a[ prop ] = b[ prop ];
  }
  return a;
}

var arraySlice = Array.prototype.slice;

// turn element or nodeList into an array
function makeArray( obj ) {
  if ( Array.isArray( obj ) ) {
    // use object if already an array
    return obj;
  }

  var isArrayLike = typeof obj == 'object' && typeof obj.length == 'number';
  if ( isArrayLike ) {
    // convert nodeList to array
    return arraySlice.call( obj );
  }

  // array of single index
  return [ obj ];
}

// -------------------------- imagesLoaded -------------------------- //

/**
 * @param {Array, Element, NodeList, String} elem
 * @param {Object or Function} options - if function, use as callback
 * @param {Function} onAlways - callback function
 */
function ImagesLoaded( elem, options, onAlways ) {
  // coerce ImagesLoaded() without new, to be new ImagesLoaded()
  if ( !( this instanceof ImagesLoaded ) ) {
    return new ImagesLoaded( elem, options, onAlways );
  }
  // use elem as selector string
  var queryElem = elem;
  if ( typeof elem == 'string' ) {
    queryElem = document.querySelectorAll( elem );
  }
  // bail if bad element
  if ( !queryElem ) {
    console.error( 'Bad element for imagesLoaded ' + ( queryElem || elem ) );
    return;
  }

  this.elements = makeArray( queryElem );
  this.options = extend( {}, this.options );
  // shift arguments if no options set
  if ( typeof options == 'function' ) {
    onAlways = options;
  } else {
    extend( this.options, options );
  }

  if ( onAlways ) {
    this.on( 'always', onAlways );
  }

  this.getImages();

  if ( $ ) {
    // add jQuery Deferred object
    this.jqDeferred = new $.Deferred();
  }

  // HACK check async to allow time to bind listeners
  setTimeout( this.check.bind( this ) );
}

ImagesLoaded.prototype = Object.create( EvEmitter.prototype );

ImagesLoaded.prototype.options = {};

ImagesLoaded.prototype.getImages = function() {
  this.images = [];

  // filter & find items if we have an item selector
  this.elements.forEach( this.addElementImages, this );
};

/**
 * @param {Node} element
 */
ImagesLoaded.prototype.addElementImages = function( elem ) {
  // filter siblings
  if ( elem.nodeName == 'IMG' ) {
    this.addImage( elem );
  }
  // get background image on element
  if ( this.options.background === true ) {
    this.addElementBackgroundImages( elem );
  }

  // find children
  // no non-element nodes, #143
  var nodeType = elem.nodeType;
  if ( !nodeType || !elementNodeTypes[ nodeType ] ) {
    return;
  }
  var childImgs = elem.querySelectorAll('img');
  // concat childElems to filterFound array
  for ( var i=0; i < childImgs.length; i++ ) {
    var img = childImgs[i];
    this.addImage( img );
  }

  // get child background images
  if ( typeof this.options.background == 'string' ) {
    var children = elem.querySelectorAll( this.options.background );
    for ( i=0; i < children.length; i++ ) {
      var child = children[i];
      this.addElementBackgroundImages( child );
    }
  }
};

var elementNodeTypes = {
  1: true,
  9: true,
  11: true
};

ImagesLoaded.prototype.addElementBackgroundImages = function( elem ) {
  var style = getComputedStyle( elem );
  if ( !style ) {
    // Firefox returns null if in a hidden iframe https://bugzil.la/548397
    return;
  }
  // get url inside url("...")
  var reURL = /url\((['"])?(.*?)\1\)/gi;
  var matches = reURL.exec( style.backgroundImage );
  while ( matches !== null ) {
    var url = matches && matches[2];
    if ( url ) {
      this.addBackground( url, elem );
    }
    matches = reURL.exec( style.backgroundImage );
  }
};

/**
 * @param {Image} img
 */
ImagesLoaded.prototype.addImage = function( img ) {
  var loadingImage = new LoadingImage( img );
  this.images.push( loadingImage );
};

ImagesLoaded.prototype.addBackground = function( url, elem ) {
  var background = new Background( url, elem );
  this.images.push( background );
};

ImagesLoaded.prototype.check = function() {
  var _this = this;
  this.progressedCount = 0;
  this.hasAnyBroken = false;
  // complete if no images
  if ( !this.images.length ) {
    this.complete();
    return;
  }

  function onProgress( image, elem, message ) {
    // HACK - Chrome triggers event before object properties have changed. #83
    setTimeout( function() {
      _this.progress( image, elem, message );
    });
  }

  this.images.forEach( function( loadingImage ) {
    loadingImage.once( 'progress', onProgress );
    loadingImage.check();
  });
};

ImagesLoaded.prototype.progress = function( image, elem, message ) {
  this.progressedCount++;
  this.hasAnyBroken = this.hasAnyBroken || !image.isLoaded;
  // progress event
  this.emitEvent( 'progress', [ this, image, elem ] );
  if ( this.jqDeferred && this.jqDeferred.notify ) {
    this.jqDeferred.notify( this, image );
  }
  // check if completed
  if ( this.progressedCount == this.images.length ) {
    this.complete();
  }

  if ( this.options.debug && console ) {
    console.log( 'progress: ' + message, image, elem );
  }
};

ImagesLoaded.prototype.complete = function() {
  var eventName = this.hasAnyBroken ? 'fail' : 'done';
  this.isComplete = true;
  this.emitEvent( eventName, [ this ] );
  this.emitEvent( 'always', [ this ] );
  if ( this.jqDeferred ) {
    var jqMethod = this.hasAnyBroken ? 'reject' : 'resolve';
    this.jqDeferred[ jqMethod ]( this );
  }
};

// --------------------------  -------------------------- //

function LoadingImage( img ) {
  this.img = img;
}

LoadingImage.prototype = Object.create( EvEmitter.prototype );

LoadingImage.prototype.check = function() {
  // If complete is true and browser supports natural sizes,
  // try to check for image status manually.
  var isComplete = this.getIsImageComplete();
  if ( isComplete ) {
    // report based on naturalWidth
    this.confirm( this.img.naturalWidth !== 0, 'naturalWidth' );
    return;
  }

  // If none of the checks above matched, simulate loading on detached element.
  this.proxyImage = new Image();
  this.proxyImage.addEventListener( 'load', this );
  this.proxyImage.addEventListener( 'error', this );
  // bind to image as well for Firefox. #191
  this.img.addEventListener( 'load', this );
  this.img.addEventListener( 'error', this );
  this.proxyImage.src = this.img.src;
};

LoadingImage.prototype.getIsImageComplete = function() {
  // check for non-zero, non-undefined naturalWidth
  // fixes Safari+InfiniteScroll+Masonry bug infinite-scroll#671
  return this.img.complete && this.img.naturalWidth;
};

LoadingImage.prototype.confirm = function( isLoaded, message ) {
  this.isLoaded = isLoaded;
  this.emitEvent( 'progress', [ this, this.img, message ] );
};

// ----- events ----- //

// trigger specified handler for event type
LoadingImage.prototype.handleEvent = function( event ) {
  var method = 'on' + event.type;
  if ( this[ method ] ) {
    this[ method ]( event );
  }
};

LoadingImage.prototype.onload = function() {
  this.confirm( true, 'onload' );
  this.unbindEvents();
};

LoadingImage.prototype.onerror = function() {
  this.confirm( false, 'onerror' );
  this.unbindEvents();
};

LoadingImage.prototype.unbindEvents = function() {
  this.proxyImage.removeEventListener( 'load', this );
  this.proxyImage.removeEventListener( 'error', this );
  this.img.removeEventListener( 'load', this );
  this.img.removeEventListener( 'error', this );
};

// -------------------------- Background -------------------------- //

function Background( url, element ) {
  this.url = url;
  this.element = element;
  this.img = new Image();
}

// inherit LoadingImage prototype
Background.prototype = Object.create( LoadingImage.prototype );

Background.prototype.check = function() {
  this.img.addEventListener( 'load', this );
  this.img.addEventListener( 'error', this );
  this.img.src = this.url;
  // check if image is already complete
  var isComplete = this.getIsImageComplete();
  if ( isComplete ) {
    this.confirm( this.img.naturalWidth !== 0, 'naturalWidth' );
    this.unbindEvents();
  }
};

Background.prototype.unbindEvents = function() {
  this.img.removeEventListener( 'load', this );
  this.img.removeEventListener( 'error', this );
};

Background.prototype.confirm = function( isLoaded, message ) {
  this.isLoaded = isLoaded;
  this.emitEvent( 'progress', [ this, this.element, message ] );
};

// -------------------------- jQuery -------------------------- //

ImagesLoaded.makeJQueryPlugin = function( jQuery ) {
  jQuery = jQuery || window.jQuery;
  if ( !jQuery ) {
    return;
  }
  // set local variable
  $ = jQuery;
  // $().imagesLoaded()
  $.fn.imagesLoaded = function( options, callback ) {
    var instance = new ImagesLoaded( this, options, callback );
    return instance.jqDeferred.promise( $(this) );
  };
};
// try making plugin
ImagesLoaded.makeJQueryPlugin();

// --------------------------  -------------------------- //

return ImagesLoaded;

});


/***/ }),

/***/ "./node_modules/jquery/dist/jquery.js":
/*!********************************************!*\
  !*** ./node_modules/jquery/dist/jquery.js ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
 * jQuery JavaScript Library v3.5.1
 * https://jquery.com/
 *
 * Includes Sizzle.js
 * https://sizzlejs.com/
 *
 * Copyright JS Foundation and other contributors
 * Released under the MIT license
 * https://jquery.org/license
 *
 * Date: 2020-05-04T22:49Z
 */
( function( global, factory ) {

	"use strict";

	if (  true && typeof module.exports === "object" ) {

		// For CommonJS and CommonJS-like environments where a proper `window`
		// is present, execute the factory and get jQuery.
		// For environments that do not have a `window` with a `document`
		// (such as Node.js), expose a factory as module.exports.
		// This accentuates the need for the creation of a real `window`.
		// e.g. var jQuery = require("jquery")(window);
		// See ticket #14549 for more info.
		module.exports = global.document ?
			factory( global, true ) :
			function( w ) {
				if ( !w.document ) {
					throw new Error( "jQuery requires a window with a document" );
				}
				return factory( w );
			};
	} else {
		factory( global );
	}

// Pass this if window is not defined yet
} )( typeof window !== "undefined" ? window : this, function( window, noGlobal ) {

// Edge <= 12 - 13+, Firefox <=18 - 45+, IE 10 - 11, Safari 5.1 - 9+, iOS 6 - 9.1
// throw exceptions when non-strict code (e.g., ASP.NET 4.5) accesses strict mode
// arguments.callee.caller (trac-13335). But as of jQuery 3.0 (2016), strict mode should be common
// enough that all such attempts are guarded in a try block.
"use strict";

var arr = [];

var getProto = Object.getPrototypeOf;

var slice = arr.slice;

var flat = arr.flat ? function( array ) {
	return arr.flat.call( array );
} : function( array ) {
	return arr.concat.apply( [], array );
};


var push = arr.push;

var indexOf = arr.indexOf;

var class2type = {};

var toString = class2type.toString;

var hasOwn = class2type.hasOwnProperty;

var fnToString = hasOwn.toString;

var ObjectFunctionString = fnToString.call( Object );

var support = {};

var isFunction = function isFunction( obj ) {

      // Support: Chrome <=57, Firefox <=52
      // In some browsers, typeof returns "function" for HTML <object> elements
      // (i.e., `typeof document.createElement( "object" ) === "function"`).
      // We don't want to classify *any* DOM node as a function.
      return typeof obj === "function" && typeof obj.nodeType !== "number";
  };


var isWindow = function isWindow( obj ) {
		return obj != null && obj === obj.window;
	};


var document = window.document;



	var preservedScriptAttributes = {
		type: true,
		src: true,
		nonce: true,
		noModule: true
	};

	function DOMEval( code, node, doc ) {
		doc = doc || document;

		var i, val,
			script = doc.createElement( "script" );

		script.text = code;
		if ( node ) {
			for ( i in preservedScriptAttributes ) {

				// Support: Firefox 64+, Edge 18+
				// Some browsers don't support the "nonce" property on scripts.
				// On the other hand, just using `getAttribute` is not enough as
				// the `nonce` attribute is reset to an empty string whenever it
				// becomes browsing-context connected.
				// See https://github.com/whatwg/html/issues/2369
				// See https://html.spec.whatwg.org/#nonce-attributes
				// The `node.getAttribute` check was added for the sake of
				// `jQuery.globalEval` so that it can fake a nonce-containing node
				// via an object.
				val = node[ i ] || node.getAttribute && node.getAttribute( i );
				if ( val ) {
					script.setAttribute( i, val );
				}
			}
		}
		doc.head.appendChild( script ).parentNode.removeChild( script );
	}


function toType( obj ) {
	if ( obj == null ) {
		return obj + "";
	}

	// Support: Android <=2.3 only (functionish RegExp)
	return typeof obj === "object" || typeof obj === "function" ?
		class2type[ toString.call( obj ) ] || "object" :
		typeof obj;
}
/* global Symbol */
// Defining this global in .eslintrc.json would create a danger of using the global
// unguarded in another place, it seems safer to define global only for this module



var
	version = "3.5.1",

	// Define a local copy of jQuery
	jQuery = function( selector, context ) {

		// The jQuery object is actually just the init constructor 'enhanced'
		// Need init if jQuery is called (just allow error to be thrown if not included)
		return new jQuery.fn.init( selector, context );
	};

jQuery.fn = jQuery.prototype = {

	// The current version of jQuery being used
	jquery: version,

	constructor: jQuery,

	// The default length of a jQuery object is 0
	length: 0,

	toArray: function() {
		return slice.call( this );
	},

	// Get the Nth element in the matched element set OR
	// Get the whole matched element set as a clean array
	get: function( num ) {

		// Return all the elements in a clean array
		if ( num == null ) {
			return slice.call( this );
		}

		// Return just the one element from the set
		return num < 0 ? this[ num + this.length ] : this[ num ];
	},

	// Take an array of elements and push it onto the stack
	// (returning the new matched element set)
	pushStack: function( elems ) {

		// Build a new jQuery matched element set
		var ret = jQuery.merge( this.constructor(), elems );

		// Add the old object onto the stack (as a reference)
		ret.prevObject = this;

		// Return the newly-formed element set
		return ret;
	},

	// Execute a callback for every element in the matched set.
	each: function( callback ) {
		return jQuery.each( this, callback );
	},

	map: function( callback ) {
		return this.pushStack( jQuery.map( this, function( elem, i ) {
			return callback.call( elem, i, elem );
		} ) );
	},

	slice: function() {
		return this.pushStack( slice.apply( this, arguments ) );
	},

	first: function() {
		return this.eq( 0 );
	},

	last: function() {
		return this.eq( -1 );
	},

	even: function() {
		return this.pushStack( jQuery.grep( this, function( _elem, i ) {
			return ( i + 1 ) % 2;
		} ) );
	},

	odd: function() {
		return this.pushStack( jQuery.grep( this, function( _elem, i ) {
			return i % 2;
		} ) );
	},

	eq: function( i ) {
		var len = this.length,
			j = +i + ( i < 0 ? len : 0 );
		return this.pushStack( j >= 0 && j < len ? [ this[ j ] ] : [] );
	},

	end: function() {
		return this.prevObject || this.constructor();
	},

	// For internal use only.
	// Behaves like an Array's method, not like a jQuery method.
	push: push,
	sort: arr.sort,
	splice: arr.splice
};

jQuery.extend = jQuery.fn.extend = function() {
	var options, name, src, copy, copyIsArray, clone,
		target = arguments[ 0 ] || {},
		i = 1,
		length = arguments.length,
		deep = false;

	// Handle a deep copy situation
	if ( typeof target === "boolean" ) {
		deep = target;

		// Skip the boolean and the target
		target = arguments[ i ] || {};
		i++;
	}

	// Handle case when target is a string or something (possible in deep copy)
	if ( typeof target !== "object" && !isFunction( target ) ) {
		target = {};
	}

	// Extend jQuery itself if only one argument is passed
	if ( i === length ) {
		target = this;
		i--;
	}

	for ( ; i < length; i++ ) {

		// Only deal with non-null/undefined values
		if ( ( options = arguments[ i ] ) != null ) {

			// Extend the base object
			for ( name in options ) {
				copy = options[ name ];

				// Prevent Object.prototype pollution
				// Prevent never-ending loop
				if ( name === "__proto__" || target === copy ) {
					continue;
				}

				// Recurse if we're merging plain objects or arrays
				if ( deep && copy && ( jQuery.isPlainObject( copy ) ||
					( copyIsArray = Array.isArray( copy ) ) ) ) {
					src = target[ name ];

					// Ensure proper type for the source value
					if ( copyIsArray && !Array.isArray( src ) ) {
						clone = [];
					} else if ( !copyIsArray && !jQuery.isPlainObject( src ) ) {
						clone = {};
					} else {
						clone = src;
					}
					copyIsArray = false;

					// Never move original objects, clone them
					target[ name ] = jQuery.extend( deep, clone, copy );

				// Don't bring in undefined values
				} else if ( copy !== undefined ) {
					target[ name ] = copy;
				}
			}
		}
	}

	// Return the modified object
	return target;
};

jQuery.extend( {

	// Unique for each copy of jQuery on the page
	expando: "jQuery" + ( version + Math.random() ).replace( /\D/g, "" ),

	// Assume jQuery is ready without the ready module
	isReady: true,

	error: function( msg ) {
		throw new Error( msg );
	},

	noop: function() {},

	isPlainObject: function( obj ) {
		var proto, Ctor;

		// Detect obvious negatives
		// Use toString instead of jQuery.type to catch host objects
		if ( !obj || toString.call( obj ) !== "[object Object]" ) {
			return false;
		}

		proto = getProto( obj );

		// Objects with no prototype (e.g., `Object.create( null )`) are plain
		if ( !proto ) {
			return true;
		}

		// Objects with prototype are plain iff they were constructed by a global Object function
		Ctor = hasOwn.call( proto, "constructor" ) && proto.constructor;
		return typeof Ctor === "function" && fnToString.call( Ctor ) === ObjectFunctionString;
	},

	isEmptyObject: function( obj ) {
		var name;

		for ( name in obj ) {
			return false;
		}
		return true;
	},

	// Evaluates a script in a provided context; falls back to the global one
	// if not specified.
	globalEval: function( code, options, doc ) {
		DOMEval( code, { nonce: options && options.nonce }, doc );
	},

	each: function( obj, callback ) {
		var length, i = 0;

		if ( isArrayLike( obj ) ) {
			length = obj.length;
			for ( ; i < length; i++ ) {
				if ( callback.call( obj[ i ], i, obj[ i ] ) === false ) {
					break;
				}
			}
		} else {
			for ( i in obj ) {
				if ( callback.call( obj[ i ], i, obj[ i ] ) === false ) {
					break;
				}
			}
		}

		return obj;
	},

	// results is for internal usage only
	makeArray: function( arr, results ) {
		var ret = results || [];

		if ( arr != null ) {
			if ( isArrayLike( Object( arr ) ) ) {
				jQuery.merge( ret,
					typeof arr === "string" ?
					[ arr ] : arr
				);
			} else {
				push.call( ret, arr );
			}
		}

		return ret;
	},

	inArray: function( elem, arr, i ) {
		return arr == null ? -1 : indexOf.call( arr, elem, i );
	},

	// Support: Android <=4.0 only, PhantomJS 1 only
	// push.apply(_, arraylike) throws on ancient WebKit
	merge: function( first, second ) {
		var len = +second.length,
			j = 0,
			i = first.length;

		for ( ; j < len; j++ ) {
			first[ i++ ] = second[ j ];
		}

		first.length = i;

		return first;
	},

	grep: function( elems, callback, invert ) {
		var callbackInverse,
			matches = [],
			i = 0,
			length = elems.length,
			callbackExpect = !invert;

		// Go through the array, only saving the items
		// that pass the validator function
		for ( ; i < length; i++ ) {
			callbackInverse = !callback( elems[ i ], i );
			if ( callbackInverse !== callbackExpect ) {
				matches.push( elems[ i ] );
			}
		}

		return matches;
	},

	// arg is for internal usage only
	map: function( elems, callback, arg ) {
		var length, value,
			i = 0,
			ret = [];

		// Go through the array, translating each of the items to their new values
		if ( isArrayLike( elems ) ) {
			length = elems.length;
			for ( ; i < length; i++ ) {
				value = callback( elems[ i ], i, arg );

				if ( value != null ) {
					ret.push( value );
				}
			}

		// Go through every key on the object,
		} else {
			for ( i in elems ) {
				value = callback( elems[ i ], i, arg );

				if ( value != null ) {
					ret.push( value );
				}
			}
		}

		// Flatten any nested arrays
		return flat( ret );
	},

	// A global GUID counter for objects
	guid: 1,

	// jQuery.support is not used in Core but other projects attach their
	// properties to it so it needs to exist.
	support: support
} );

if ( typeof Symbol === "function" ) {
	jQuery.fn[ Symbol.iterator ] = arr[ Symbol.iterator ];
}

// Populate the class2type map
jQuery.each( "Boolean Number String Function Array Date RegExp Object Error Symbol".split( " " ),
function( _i, name ) {
	class2type[ "[object " + name + "]" ] = name.toLowerCase();
} );

function isArrayLike( obj ) {

	// Support: real iOS 8.2 only (not reproducible in simulator)
	// `in` check used to prevent JIT error (gh-2145)
	// hasOwn isn't used here due to false negatives
	// regarding Nodelist length in IE
	var length = !!obj && "length" in obj && obj.length,
		type = toType( obj );

	if ( isFunction( obj ) || isWindow( obj ) ) {
		return false;
	}

	return type === "array" || length === 0 ||
		typeof length === "number" && length > 0 && ( length - 1 ) in obj;
}
var Sizzle =
/*!
 * Sizzle CSS Selector Engine v2.3.5
 * https://sizzlejs.com/
 *
 * Copyright JS Foundation and other contributors
 * Released under the MIT license
 * https://js.foundation/
 *
 * Date: 2020-03-14
 */
( function( window ) {
var i,
	support,
	Expr,
	getText,
	isXML,
	tokenize,
	compile,
	select,
	outermostContext,
	sortInput,
	hasDuplicate,

	// Local document vars
	setDocument,
	document,
	docElem,
	documentIsHTML,
	rbuggyQSA,
	rbuggyMatches,
	matches,
	contains,

	// Instance-specific data
	expando = "sizzle" + 1 * new Date(),
	preferredDoc = window.document,
	dirruns = 0,
	done = 0,
	classCache = createCache(),
	tokenCache = createCache(),
	compilerCache = createCache(),
	nonnativeSelectorCache = createCache(),
	sortOrder = function( a, b ) {
		if ( a === b ) {
			hasDuplicate = true;
		}
		return 0;
	},

	// Instance methods
	hasOwn = ( {} ).hasOwnProperty,
	arr = [],
	pop = arr.pop,
	pushNative = arr.push,
	push = arr.push,
	slice = arr.slice,

	// Use a stripped-down indexOf as it's faster than native
	// https://jsperf.com/thor-indexof-vs-for/5
	indexOf = function( list, elem ) {
		var i = 0,
			len = list.length;
		for ( ; i < len; i++ ) {
			if ( list[ i ] === elem ) {
				return i;
			}
		}
		return -1;
	},

	booleans = "checked|selected|async|autofocus|autoplay|controls|defer|disabled|hidden|" +
		"ismap|loop|multiple|open|readonly|required|scoped",

	// Regular expressions

	// http://www.w3.org/TR/css3-selectors/#whitespace
	whitespace = "[\\x20\\t\\r\\n\\f]",

	// https://www.w3.org/TR/css-syntax-3/#ident-token-diagram
	identifier = "(?:\\\\[\\da-fA-F]{1,6}" + whitespace +
		"?|\\\\[^\\r\\n\\f]|[\\w-]|[^\0-\\x7f])+",

	// Attribute selectors: http://www.w3.org/TR/selectors/#attribute-selectors
	attributes = "\\[" + whitespace + "*(" + identifier + ")(?:" + whitespace +

		// Operator (capture 2)
		"*([*^$|!~]?=)" + whitespace +

		// "Attribute values must be CSS identifiers [capture 5]
		// or strings [capture 3 or capture 4]"
		"*(?:'((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\"|(" + identifier + "))|)" +
		whitespace + "*\\]",

	pseudos = ":(" + identifier + ")(?:\\((" +

		// To reduce the number of selectors needing tokenize in the preFilter, prefer arguments:
		// 1. quoted (capture 3; capture 4 or capture 5)
		"('((?:\\\\.|[^\\\\'])*)'|\"((?:\\\\.|[^\\\\\"])*)\")|" +

		// 2. simple (capture 6)
		"((?:\\\\.|[^\\\\()[\\]]|" + attributes + ")*)|" +

		// 3. anything else (capture 2)
		".*" +
		")\\)|)",

	// Leading and non-escaped trailing whitespace, capturing some non-whitespace characters preceding the latter
	rwhitespace = new RegExp( whitespace + "+", "g" ),
	rtrim = new RegExp( "^" + whitespace + "+|((?:^|[^\\\\])(?:\\\\.)*)" +
		whitespace + "+$", "g" ),

	rcomma = new RegExp( "^" + whitespace + "*," + whitespace + "*" ),
	rcombinators = new RegExp( "^" + whitespace + "*([>+~]|" + whitespace + ")" + whitespace +
		"*" ),
	rdescend = new RegExp( whitespace + "|>" ),

	rpseudo = new RegExp( pseudos ),
	ridentifier = new RegExp( "^" + identifier + "$" ),

	matchExpr = {
		"ID": new RegExp( "^#(" + identifier + ")" ),
		"CLASS": new RegExp( "^\\.(" + identifier + ")" ),
		"TAG": new RegExp( "^(" + identifier + "|[*])" ),
		"ATTR": new RegExp( "^" + attributes ),
		"PSEUDO": new RegExp( "^" + pseudos ),
		"CHILD": new RegExp( "^:(only|first|last|nth|nth-last)-(child|of-type)(?:\\(" +
			whitespace + "*(even|odd|(([+-]|)(\\d*)n|)" + whitespace + "*(?:([+-]|)" +
			whitespace + "*(\\d+)|))" + whitespace + "*\\)|)", "i" ),
		"bool": new RegExp( "^(?:" + booleans + ")$", "i" ),

		// For use in libraries implementing .is()
		// We use this for POS matching in `select`
		"needsContext": new RegExp( "^" + whitespace +
			"*[>+~]|:(even|odd|eq|gt|lt|nth|first|last)(?:\\(" + whitespace +
			"*((?:-\\d)?\\d*)" + whitespace + "*\\)|)(?=[^-]|$)", "i" )
	},

	rhtml = /HTML$/i,
	rinputs = /^(?:input|select|textarea|button)$/i,
	rheader = /^h\d$/i,

	rnative = /^[^{]+\{\s*\[native \w/,

	// Easily-parseable/retrievable ID or TAG or CLASS selectors
	rquickExpr = /^(?:#([\w-]+)|(\w+)|\.([\w-]+))$/,

	rsibling = /[+~]/,

	// CSS escapes
	// http://www.w3.org/TR/CSS21/syndata.html#escaped-characters
	runescape = new RegExp( "\\\\[\\da-fA-F]{1,6}" + whitespace + "?|\\\\([^\\r\\n\\f])", "g" ),
	funescape = function( escape, nonHex ) {
		var high = "0x" + escape.slice( 1 ) - 0x10000;

		return nonHex ?

			// Strip the backslash prefix from a non-hex escape sequence
			nonHex :

			// Replace a hexadecimal escape sequence with the encoded Unicode code point
			// Support: IE <=11+
			// For values outside the Basic Multilingual Plane (BMP), manually construct a
			// surrogate pair
			high < 0 ?
				String.fromCharCode( high + 0x10000 ) :
				String.fromCharCode( high >> 10 | 0xD800, high & 0x3FF | 0xDC00 );
	},

	// CSS string/identifier serialization
	// https://drafts.csswg.org/cssom/#common-serializing-idioms
	rcssescape = /([\0-\x1f\x7f]|^-?\d)|^-$|[^\0-\x1f\x7f-\uFFFF\w-]/g,
	fcssescape = function( ch, asCodePoint ) {
		if ( asCodePoint ) {

			// U+0000 NULL becomes U+FFFD REPLACEMENT CHARACTER
			if ( ch === "\0" ) {
				return "\uFFFD";
			}

			// Control characters and (dependent upon position) numbers get escaped as code points
			return ch.slice( 0, -1 ) + "\\" +
				ch.charCodeAt( ch.length - 1 ).toString( 16 ) + " ";
		}

		// Other potentially-special ASCII characters get backslash-escaped
		return "\\" + ch;
	},

	// Used for iframes
	// See setDocument()
	// Removing the function wrapper causes a "Permission Denied"
	// error in IE
	unloadHandler = function() {
		setDocument();
	},

	inDisabledFieldset = addCombinator(
		function( elem ) {
			return elem.disabled === true && elem.nodeName.toLowerCase() === "fieldset";
		},
		{ dir: "parentNode", next: "legend" }
	);

// Optimize for push.apply( _, NodeList )
try {
	push.apply(
		( arr = slice.call( preferredDoc.childNodes ) ),
		preferredDoc.childNodes
	);

	// Support: Android<4.0
	// Detect silently failing push.apply
	// eslint-disable-next-line no-unused-expressions
	arr[ preferredDoc.childNodes.length ].nodeType;
} catch ( e ) {
	push = { apply: arr.length ?

		// Leverage slice if possible
		function( target, els ) {
			pushNative.apply( target, slice.call( els ) );
		} :

		// Support: IE<9
		// Otherwise append directly
		function( target, els ) {
			var j = target.length,
				i = 0;

			// Can't trust NodeList.length
			while ( ( target[ j++ ] = els[ i++ ] ) ) {}
			target.length = j - 1;
		}
	};
}

function Sizzle( selector, context, results, seed ) {
	var m, i, elem, nid, match, groups, newSelector,
		newContext = context && context.ownerDocument,

		// nodeType defaults to 9, since context defaults to document
		nodeType = context ? context.nodeType : 9;

	results = results || [];

	// Return early from calls with invalid selector or context
	if ( typeof selector !== "string" || !selector ||
		nodeType !== 1 && nodeType !== 9 && nodeType !== 11 ) {

		return results;
	}

	// Try to shortcut find operations (as opposed to filters) in HTML documents
	if ( !seed ) {
		setDocument( context );
		context = context || document;

		if ( documentIsHTML ) {

			// If the selector is sufficiently simple, try using a "get*By*" DOM method
			// (excepting DocumentFragment context, where the methods don't exist)
			if ( nodeType !== 11 && ( match = rquickExpr.exec( selector ) ) ) {

				// ID selector
				if ( ( m = match[ 1 ] ) ) {

					// Document context
					if ( nodeType === 9 ) {
						if ( ( elem = context.getElementById( m ) ) ) {

							// Support: IE, Opera, Webkit
							// TODO: identify versions
							// getElementById can match elements by name instead of ID
							if ( elem.id === m ) {
								results.push( elem );
								return results;
							}
						} else {
							return results;
						}

					// Element context
					} else {

						// Support: IE, Opera, Webkit
						// TODO: identify versions
						// getElementById can match elements by name instead of ID
						if ( newContext && ( elem = newContext.getElementById( m ) ) &&
							contains( context, elem ) &&
							elem.id === m ) {

							results.push( elem );
							return results;
						}
					}

				// Type selector
				} else if ( match[ 2 ] ) {
					push.apply( results, context.getElementsByTagName( selector ) );
					return results;

				// Class selector
				} else if ( ( m = match[ 3 ] ) && support.getElementsByClassName &&
					context.getElementsByClassName ) {

					push.apply( results, context.getElementsByClassName( m ) );
					return results;
				}
			}

			// Take advantage of querySelectorAll
			if ( support.qsa &&
				!nonnativeSelectorCache[ selector + " " ] &&
				( !rbuggyQSA || !rbuggyQSA.test( selector ) ) &&

				// Support: IE 8 only
				// Exclude object elements
				( nodeType !== 1 || context.nodeName.toLowerCase() !== "object" ) ) {

				newSelector = selector;
				newContext = context;

				// qSA considers elements outside a scoping root when evaluating child or
				// descendant combinators, which is not what we want.
				// In such cases, we work around the behavior by prefixing every selector in the
				// list with an ID selector referencing the scope context.
				// The technique has to be used as well when a leading combinator is used
				// as such selectors are not recognized by querySelectorAll.
				// Thanks to Andrew Dupont for this technique.
				if ( nodeType === 1 &&
					( rdescend.test( selector ) || rcombinators.test( selector ) ) ) {

					// Expand context for sibling selectors
					newContext = rsibling.test( selector ) && testContext( context.parentNode ) ||
						context;

					// We can use :scope instead of the ID hack if the browser
					// supports it & if we're not changing the context.
					if ( newContext !== context || !support.scope ) {

						// Capture the context ID, setting it first if necessary
						if ( ( nid = context.getAttribute( "id" ) ) ) {
							nid = nid.replace( rcssescape, fcssescape );
						} else {
							context.setAttribute( "id", ( nid = expando ) );
						}
					}

					// Prefix every selector in the list
					groups = tokenize( selector );
					i = groups.length;
					while ( i-- ) {
						groups[ i ] = ( nid ? "#" + nid : ":scope" ) + " " +
							toSelector( groups[ i ] );
					}
					newSelector = groups.join( "," );
				}

				try {
					push.apply( results,
						newContext.querySelectorAll( newSelector )
					);
					return results;
				} catch ( qsaError ) {
					nonnativeSelectorCache( selector, true );
				} finally {
					if ( nid === expando ) {
						context.removeAttribute( "id" );
					}
				}
			}
		}
	}

	// All others
	return select( selector.replace( rtrim, "$1" ), context, results, seed );
}

/**
 * Create key-value caches of limited size
 * @returns {function(string, object)} Returns the Object data after storing it on itself with
 *	property name the (space-suffixed) string and (if the cache is larger than Expr.cacheLength)
 *	deleting the oldest entry
 */
function createCache() {
	var keys = [];

	function cache( key, value ) {

		// Use (key + " ") to avoid collision with native prototype properties (see Issue #157)
		if ( keys.push( key + " " ) > Expr.cacheLength ) {

			// Only keep the most recent entries
			delete cache[ keys.shift() ];
		}
		return ( cache[ key + " " ] = value );
	}
	return cache;
}

/**
 * Mark a function for special use by Sizzle
 * @param {Function} fn The function to mark
 */
function markFunction( fn ) {
	fn[ expando ] = true;
	return fn;
}

/**
 * Support testing using an element
 * @param {Function} fn Passed the created element and returns a boolean result
 */
function assert( fn ) {
	var el = document.createElement( "fieldset" );

	try {
		return !!fn( el );
	} catch ( e ) {
		return false;
	} finally {

		// Remove from its parent by default
		if ( el.parentNode ) {
			el.parentNode.removeChild( el );
		}

		// release memory in IE
		el = null;
	}
}

/**
 * Adds the same handler for all of the specified attrs
 * @param {String} attrs Pipe-separated list of attributes
 * @param {Function} handler The method that will be applied
 */
function addHandle( attrs, handler ) {
	var arr = attrs.split( "|" ),
		i = arr.length;

	while ( i-- ) {
		Expr.attrHandle[ arr[ i ] ] = handler;
	}
}

/**
 * Checks document order of two siblings
 * @param {Element} a
 * @param {Element} b
 * @returns {Number} Returns less than 0 if a precedes b, greater than 0 if a follows b
 */
function siblingCheck( a, b ) {
	var cur = b && a,
		diff = cur && a.nodeType === 1 && b.nodeType === 1 &&
			a.sourceIndex - b.sourceIndex;

	// Use IE sourceIndex if available on both nodes
	if ( diff ) {
		return diff;
	}

	// Check if b follows a
	if ( cur ) {
		while ( ( cur = cur.nextSibling ) ) {
			if ( cur === b ) {
				return -1;
			}
		}
	}

	return a ? 1 : -1;
}

/**
 * Returns a function to use in pseudos for input types
 * @param {String} type
 */
function createInputPseudo( type ) {
	return function( elem ) {
		var name = elem.nodeName.toLowerCase();
		return name === "input" && elem.type === type;
	};
}

/**
 * Returns a function to use in pseudos for buttons
 * @param {String} type
 */
function createButtonPseudo( type ) {
	return function( elem ) {
		var name = elem.nodeName.toLowerCase();
		return ( name === "input" || name === "button" ) && elem.type === type;
	};
}

/**
 * Returns a function to use in pseudos for :enabled/:disabled
 * @param {Boolean} disabled true for :disabled; false for :enabled
 */
function createDisabledPseudo( disabled ) {

	// Known :disabled false positives: fieldset[disabled] > legend:nth-of-type(n+2) :can-disable
	return function( elem ) {

		// Only certain elements can match :enabled or :disabled
		// https://html.spec.whatwg.org/multipage/scripting.html#selector-enabled
		// https://html.spec.whatwg.org/multipage/scripting.html#selector-disabled
		if ( "form" in elem ) {

			// Check for inherited disabledness on relevant non-disabled elements:
			// * listed form-associated elements in a disabled fieldset
			//   https://html.spec.whatwg.org/multipage/forms.html#category-listed
			//   https://html.spec.whatwg.org/multipage/forms.html#concept-fe-disabled
			// * option elements in a disabled optgroup
			//   https://html.spec.whatwg.org/multipage/forms.html#concept-option-disabled
			// All such elements have a "form" property.
			if ( elem.parentNode && elem.disabled === false ) {

				// Option elements defer to a parent optgroup if present
				if ( "label" in elem ) {
					if ( "label" in elem.parentNode ) {
						return elem.parentNode.disabled === disabled;
					} else {
						return elem.disabled === disabled;
					}
				}

				// Support: IE 6 - 11
				// Use the isDisabled shortcut property to check for disabled fieldset ancestors
				return elem.isDisabled === disabled ||

					// Where there is no isDisabled, check manually
					/* jshint -W018 */
					elem.isDisabled !== !disabled &&
					inDisabledFieldset( elem ) === disabled;
			}

			return elem.disabled === disabled;

		// Try to winnow out elements that can't be disabled before trusting the disabled property.
		// Some victims get caught in our net (label, legend, menu, track), but it shouldn't
		// even exist on them, let alone have a boolean value.
		} else if ( "label" in elem ) {
			return elem.disabled === disabled;
		}

		// Remaining elements are neither :enabled nor :disabled
		return false;
	};
}

/**
 * Returns a function to use in pseudos for positionals
 * @param {Function} fn
 */
function createPositionalPseudo( fn ) {
	return markFunction( function( argument ) {
		argument = +argument;
		return markFunction( function( seed, matches ) {
			var j,
				matchIndexes = fn( [], seed.length, argument ),
				i = matchIndexes.length;

			// Match elements found at the specified indexes
			while ( i-- ) {
				if ( seed[ ( j = matchIndexes[ i ] ) ] ) {
					seed[ j ] = !( matches[ j ] = seed[ j ] );
				}
			}
		} );
	} );
}

/**
 * Checks a node for validity as a Sizzle context
 * @param {Element|Object=} context
 * @returns {Element|Object|Boolean} The input node if acceptable, otherwise a falsy value
 */
function testContext( context ) {
	return context && typeof context.getElementsByTagName !== "undefined" && context;
}

// Expose support vars for convenience
support = Sizzle.support = {};

/**
 * Detects XML nodes
 * @param {Element|Object} elem An element or a document
 * @returns {Boolean} True iff elem is a non-HTML XML node
 */
isXML = Sizzle.isXML = function( elem ) {
	var namespace = elem.namespaceURI,
		docElem = ( elem.ownerDocument || elem ).documentElement;

	// Support: IE <=8
	// Assume HTML when documentElement doesn't yet exist, such as inside loading iframes
	// https://bugs.jquery.com/ticket/4833
	return !rhtml.test( namespace || docElem && docElem.nodeName || "HTML" );
};

/**
 * Sets document-related variables once based on the current document
 * @param {Element|Object} [doc] An element or document object to use to set the document
 * @returns {Object} Returns the current document
 */
setDocument = Sizzle.setDocument = function( node ) {
	var hasCompare, subWindow,
		doc = node ? node.ownerDocument || node : preferredDoc;

	// Return early if doc is invalid or already selected
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( doc == document || doc.nodeType !== 9 || !doc.documentElement ) {
		return document;
	}

	// Update global variables
	document = doc;
	docElem = document.documentElement;
	documentIsHTML = !isXML( document );

	// Support: IE 9 - 11+, Edge 12 - 18+
	// Accessing iframe documents after unload throws "permission denied" errors (jQuery #13936)
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( preferredDoc != document &&
		( subWindow = document.defaultView ) && subWindow.top !== subWindow ) {

		// Support: IE 11, Edge
		if ( subWindow.addEventListener ) {
			subWindow.addEventListener( "unload", unloadHandler, false );

		// Support: IE 9 - 10 only
		} else if ( subWindow.attachEvent ) {
			subWindow.attachEvent( "onunload", unloadHandler );
		}
	}

	// Support: IE 8 - 11+, Edge 12 - 18+, Chrome <=16 - 25 only, Firefox <=3.6 - 31 only,
	// Safari 4 - 5 only, Opera <=11.6 - 12.x only
	// IE/Edge & older browsers don't support the :scope pseudo-class.
	// Support: Safari 6.0 only
	// Safari 6.0 supports :scope but it's an alias of :root there.
	support.scope = assert( function( el ) {
		docElem.appendChild( el ).appendChild( document.createElement( "div" ) );
		return typeof el.querySelectorAll !== "undefined" &&
			!el.querySelectorAll( ":scope fieldset div" ).length;
	} );

	/* Attributes
	---------------------------------------------------------------------- */

	// Support: IE<8
	// Verify that getAttribute really returns attributes and not properties
	// (excepting IE8 booleans)
	support.attributes = assert( function( el ) {
		el.className = "i";
		return !el.getAttribute( "className" );
	} );

	/* getElement(s)By*
	---------------------------------------------------------------------- */

	// Check if getElementsByTagName("*") returns only elements
	support.getElementsByTagName = assert( function( el ) {
		el.appendChild( document.createComment( "" ) );
		return !el.getElementsByTagName( "*" ).length;
	} );

	// Support: IE<9
	support.getElementsByClassName = rnative.test( document.getElementsByClassName );

	// Support: IE<10
	// Check if getElementById returns elements by name
	// The broken getElementById methods don't pick up programmatically-set names,
	// so use a roundabout getElementsByName test
	support.getById = assert( function( el ) {
		docElem.appendChild( el ).id = expando;
		return !document.getElementsByName || !document.getElementsByName( expando ).length;
	} );

	// ID filter and find
	if ( support.getById ) {
		Expr.filter[ "ID" ] = function( id ) {
			var attrId = id.replace( runescape, funescape );
			return function( elem ) {
				return elem.getAttribute( "id" ) === attrId;
			};
		};
		Expr.find[ "ID" ] = function( id, context ) {
			if ( typeof context.getElementById !== "undefined" && documentIsHTML ) {
				var elem = context.getElementById( id );
				return elem ? [ elem ] : [];
			}
		};
	} else {
		Expr.filter[ "ID" ] =  function( id ) {
			var attrId = id.replace( runescape, funescape );
			return function( elem ) {
				var node = typeof elem.getAttributeNode !== "undefined" &&
					elem.getAttributeNode( "id" );
				return node && node.value === attrId;
			};
		};

		// Support: IE 6 - 7 only
		// getElementById is not reliable as a find shortcut
		Expr.find[ "ID" ] = function( id, context ) {
			if ( typeof context.getElementById !== "undefined" && documentIsHTML ) {
				var node, i, elems,
					elem = context.getElementById( id );

				if ( elem ) {

					// Verify the id attribute
					node = elem.getAttributeNode( "id" );
					if ( node && node.value === id ) {
						return [ elem ];
					}

					// Fall back on getElementsByName
					elems = context.getElementsByName( id );
					i = 0;
					while ( ( elem = elems[ i++ ] ) ) {
						node = elem.getAttributeNode( "id" );
						if ( node && node.value === id ) {
							return [ elem ];
						}
					}
				}

				return [];
			}
		};
	}

	// Tag
	Expr.find[ "TAG" ] = support.getElementsByTagName ?
		function( tag, context ) {
			if ( typeof context.getElementsByTagName !== "undefined" ) {
				return context.getElementsByTagName( tag );

			// DocumentFragment nodes don't have gEBTN
			} else if ( support.qsa ) {
				return context.querySelectorAll( tag );
			}
		} :

		function( tag, context ) {
			var elem,
				tmp = [],
				i = 0,

				// By happy coincidence, a (broken) gEBTN appears on DocumentFragment nodes too
				results = context.getElementsByTagName( tag );

			// Filter out possible comments
			if ( tag === "*" ) {
				while ( ( elem = results[ i++ ] ) ) {
					if ( elem.nodeType === 1 ) {
						tmp.push( elem );
					}
				}

				return tmp;
			}
			return results;
		};

	// Class
	Expr.find[ "CLASS" ] = support.getElementsByClassName && function( className, context ) {
		if ( typeof context.getElementsByClassName !== "undefined" && documentIsHTML ) {
			return context.getElementsByClassName( className );
		}
	};

	/* QSA/matchesSelector
	---------------------------------------------------------------------- */

	// QSA and matchesSelector support

	// matchesSelector(:active) reports false when true (IE9/Opera 11.5)
	rbuggyMatches = [];

	// qSa(:focus) reports false when true (Chrome 21)
	// We allow this because of a bug in IE8/9 that throws an error
	// whenever `document.activeElement` is accessed on an iframe
	// So, we allow :focus to pass through QSA all the time to avoid the IE error
	// See https://bugs.jquery.com/ticket/13378
	rbuggyQSA = [];

	if ( ( support.qsa = rnative.test( document.querySelectorAll ) ) ) {

		// Build QSA regex
		// Regex strategy adopted from Diego Perini
		assert( function( el ) {

			var input;

			// Select is set to empty string on purpose
			// This is to test IE's treatment of not explicitly
			// setting a boolean content attribute,
			// since its presence should be enough
			// https://bugs.jquery.com/ticket/12359
			docElem.appendChild( el ).innerHTML = "<a id='" + expando + "'></a>" +
				"<select id='" + expando + "-\r\\' msallowcapture=''>" +
				"<option selected=''></option></select>";

			// Support: IE8, Opera 11-12.16
			// Nothing should be selected when empty strings follow ^= or $= or *=
			// The test attribute must be unknown in Opera but "safe" for WinRT
			// https://msdn.microsoft.com/en-us/library/ie/hh465388.aspx#attribute_section
			if ( el.querySelectorAll( "[msallowcapture^='']" ).length ) {
				rbuggyQSA.push( "[*^$]=" + whitespace + "*(?:''|\"\")" );
			}

			// Support: IE8
			// Boolean attributes and "value" are not treated correctly
			if ( !el.querySelectorAll( "[selected]" ).length ) {
				rbuggyQSA.push( "\\[" + whitespace + "*(?:value|" + booleans + ")" );
			}

			// Support: Chrome<29, Android<4.4, Safari<7.0+, iOS<7.0+, PhantomJS<1.9.8+
			if ( !el.querySelectorAll( "[id~=" + expando + "-]" ).length ) {
				rbuggyQSA.push( "~=" );
			}

			// Support: IE 11+, Edge 15 - 18+
			// IE 11/Edge don't find elements on a `[name='']` query in some cases.
			// Adding a temporary attribute to the document before the selection works
			// around the issue.
			// Interestingly, IE 10 & older don't seem to have the issue.
			input = document.createElement( "input" );
			input.setAttribute( "name", "" );
			el.appendChild( input );
			if ( !el.querySelectorAll( "[name='']" ).length ) {
				rbuggyQSA.push( "\\[" + whitespace + "*name" + whitespace + "*=" +
					whitespace + "*(?:''|\"\")" );
			}

			// Webkit/Opera - :checked should return selected option elements
			// http://www.w3.org/TR/2011/REC-css3-selectors-20110929/#checked
			// IE8 throws error here and will not see later tests
			if ( !el.querySelectorAll( ":checked" ).length ) {
				rbuggyQSA.push( ":checked" );
			}

			// Support: Safari 8+, iOS 8+
			// https://bugs.webkit.org/show_bug.cgi?id=136851
			// In-page `selector#id sibling-combinator selector` fails
			if ( !el.querySelectorAll( "a#" + expando + "+*" ).length ) {
				rbuggyQSA.push( ".#.+[+~]" );
			}

			// Support: Firefox <=3.6 - 5 only
			// Old Firefox doesn't throw on a badly-escaped identifier.
			el.querySelectorAll( "\\\f" );
			rbuggyQSA.push( "[\\r\\n\\f]" );
		} );

		assert( function( el ) {
			el.innerHTML = "<a href='' disabled='disabled'></a>" +
				"<select disabled='disabled'><option/></select>";

			// Support: Windows 8 Native Apps
			// The type and name attributes are restricted during .innerHTML assignment
			var input = document.createElement( "input" );
			input.setAttribute( "type", "hidden" );
			el.appendChild( input ).setAttribute( "name", "D" );

			// Support: IE8
			// Enforce case-sensitivity of name attribute
			if ( el.querySelectorAll( "[name=d]" ).length ) {
				rbuggyQSA.push( "name" + whitespace + "*[*^$|!~]?=" );
			}

			// FF 3.5 - :enabled/:disabled and hidden elements (hidden elements are still enabled)
			// IE8 throws error here and will not see later tests
			if ( el.querySelectorAll( ":enabled" ).length !== 2 ) {
				rbuggyQSA.push( ":enabled", ":disabled" );
			}

			// Support: IE9-11+
			// IE's :disabled selector does not pick up the children of disabled fieldsets
			docElem.appendChild( el ).disabled = true;
			if ( el.querySelectorAll( ":disabled" ).length !== 2 ) {
				rbuggyQSA.push( ":enabled", ":disabled" );
			}

			// Support: Opera 10 - 11 only
			// Opera 10-11 does not throw on post-comma invalid pseudos
			el.querySelectorAll( "*,:x" );
			rbuggyQSA.push( ",.*:" );
		} );
	}

	if ( ( support.matchesSelector = rnative.test( ( matches = docElem.matches ||
		docElem.webkitMatchesSelector ||
		docElem.mozMatchesSelector ||
		docElem.oMatchesSelector ||
		docElem.msMatchesSelector ) ) ) ) {

		assert( function( el ) {

			// Check to see if it's possible to do matchesSelector
			// on a disconnected node (IE 9)
			support.disconnectedMatch = matches.call( el, "*" );

			// This should fail with an exception
			// Gecko does not error, returns false instead
			matches.call( el, "[s!='']:x" );
			rbuggyMatches.push( "!=", pseudos );
		} );
	}

	rbuggyQSA = rbuggyQSA.length && new RegExp( rbuggyQSA.join( "|" ) );
	rbuggyMatches = rbuggyMatches.length && new RegExp( rbuggyMatches.join( "|" ) );

	/* Contains
	---------------------------------------------------------------------- */
	hasCompare = rnative.test( docElem.compareDocumentPosition );

	// Element contains another
	// Purposefully self-exclusive
	// As in, an element does not contain itself
	contains = hasCompare || rnative.test( docElem.contains ) ?
		function( a, b ) {
			var adown = a.nodeType === 9 ? a.documentElement : a,
				bup = b && b.parentNode;
			return a === bup || !!( bup && bup.nodeType === 1 && (
				adown.contains ?
					adown.contains( bup ) :
					a.compareDocumentPosition && a.compareDocumentPosition( bup ) & 16
			) );
		} :
		function( a, b ) {
			if ( b ) {
				while ( ( b = b.parentNode ) ) {
					if ( b === a ) {
						return true;
					}
				}
			}
			return false;
		};

	/* Sorting
	---------------------------------------------------------------------- */

	// Document order sorting
	sortOrder = hasCompare ?
	function( a, b ) {

		// Flag for duplicate removal
		if ( a === b ) {
			hasDuplicate = true;
			return 0;
		}

		// Sort on method existence if only one input has compareDocumentPosition
		var compare = !a.compareDocumentPosition - !b.compareDocumentPosition;
		if ( compare ) {
			return compare;
		}

		// Calculate position if both inputs belong to the same document
		// Support: IE 11+, Edge 17 - 18+
		// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
		// two documents; shallow comparisons work.
		// eslint-disable-next-line eqeqeq
		compare = ( a.ownerDocument || a ) == ( b.ownerDocument || b ) ?
			a.compareDocumentPosition( b ) :

			// Otherwise we know they are disconnected
			1;

		// Disconnected nodes
		if ( compare & 1 ||
			( !support.sortDetached && b.compareDocumentPosition( a ) === compare ) ) {

			// Choose the first element that is related to our preferred document
			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			// eslint-disable-next-line eqeqeq
			if ( a == document || a.ownerDocument == preferredDoc &&
				contains( preferredDoc, a ) ) {
				return -1;
			}

			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			// eslint-disable-next-line eqeqeq
			if ( b == document || b.ownerDocument == preferredDoc &&
				contains( preferredDoc, b ) ) {
				return 1;
			}

			// Maintain original order
			return sortInput ?
				( indexOf( sortInput, a ) - indexOf( sortInput, b ) ) :
				0;
		}

		return compare & 4 ? -1 : 1;
	} :
	function( a, b ) {

		// Exit early if the nodes are identical
		if ( a === b ) {
			hasDuplicate = true;
			return 0;
		}

		var cur,
			i = 0,
			aup = a.parentNode,
			bup = b.parentNode,
			ap = [ a ],
			bp = [ b ];

		// Parentless nodes are either documents or disconnected
		if ( !aup || !bup ) {

			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			/* eslint-disable eqeqeq */
			return a == document ? -1 :
				b == document ? 1 :
				/* eslint-enable eqeqeq */
				aup ? -1 :
				bup ? 1 :
				sortInput ?
				( indexOf( sortInput, a ) - indexOf( sortInput, b ) ) :
				0;

		// If the nodes are siblings, we can do a quick check
		} else if ( aup === bup ) {
			return siblingCheck( a, b );
		}

		// Otherwise we need full lists of their ancestors for comparison
		cur = a;
		while ( ( cur = cur.parentNode ) ) {
			ap.unshift( cur );
		}
		cur = b;
		while ( ( cur = cur.parentNode ) ) {
			bp.unshift( cur );
		}

		// Walk down the tree looking for a discrepancy
		while ( ap[ i ] === bp[ i ] ) {
			i++;
		}

		return i ?

			// Do a sibling check if the nodes have a common ancestor
			siblingCheck( ap[ i ], bp[ i ] ) :

			// Otherwise nodes in our document sort first
			// Support: IE 11+, Edge 17 - 18+
			// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
			// two documents; shallow comparisons work.
			/* eslint-disable eqeqeq */
			ap[ i ] == preferredDoc ? -1 :
			bp[ i ] == preferredDoc ? 1 :
			/* eslint-enable eqeqeq */
			0;
	};

	return document;
};

Sizzle.matches = function( expr, elements ) {
	return Sizzle( expr, null, null, elements );
};

Sizzle.matchesSelector = function( elem, expr ) {
	setDocument( elem );

	if ( support.matchesSelector && documentIsHTML &&
		!nonnativeSelectorCache[ expr + " " ] &&
		( !rbuggyMatches || !rbuggyMatches.test( expr ) ) &&
		( !rbuggyQSA     || !rbuggyQSA.test( expr ) ) ) {

		try {
			var ret = matches.call( elem, expr );

			// IE 9's matchesSelector returns false on disconnected nodes
			if ( ret || support.disconnectedMatch ||

				// As well, disconnected nodes are said to be in a document
				// fragment in IE 9
				elem.document && elem.document.nodeType !== 11 ) {
				return ret;
			}
		} catch ( e ) {
			nonnativeSelectorCache( expr, true );
		}
	}

	return Sizzle( expr, document, null, [ elem ] ).length > 0;
};

Sizzle.contains = function( context, elem ) {

	// Set document vars if needed
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( ( context.ownerDocument || context ) != document ) {
		setDocument( context );
	}
	return contains( context, elem );
};

Sizzle.attr = function( elem, name ) {

	// Set document vars if needed
	// Support: IE 11+, Edge 17 - 18+
	// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
	// two documents; shallow comparisons work.
	// eslint-disable-next-line eqeqeq
	if ( ( elem.ownerDocument || elem ) != document ) {
		setDocument( elem );
	}

	var fn = Expr.attrHandle[ name.toLowerCase() ],

		// Don't get fooled by Object.prototype properties (jQuery #13807)
		val = fn && hasOwn.call( Expr.attrHandle, name.toLowerCase() ) ?
			fn( elem, name, !documentIsHTML ) :
			undefined;

	return val !== undefined ?
		val :
		support.attributes || !documentIsHTML ?
			elem.getAttribute( name ) :
			( val = elem.getAttributeNode( name ) ) && val.specified ?
				val.value :
				null;
};

Sizzle.escape = function( sel ) {
	return ( sel + "" ).replace( rcssescape, fcssescape );
};

Sizzle.error = function( msg ) {
	throw new Error( "Syntax error, unrecognized expression: " + msg );
};

/**
 * Document sorting and removing duplicates
 * @param {ArrayLike} results
 */
Sizzle.uniqueSort = function( results ) {
	var elem,
		duplicates = [],
		j = 0,
		i = 0;

	// Unless we *know* we can detect duplicates, assume their presence
	hasDuplicate = !support.detectDuplicates;
	sortInput = !support.sortStable && results.slice( 0 );
	results.sort( sortOrder );

	if ( hasDuplicate ) {
		while ( ( elem = results[ i++ ] ) ) {
			if ( elem === results[ i ] ) {
				j = duplicates.push( i );
			}
		}
		while ( j-- ) {
			results.splice( duplicates[ j ], 1 );
		}
	}

	// Clear input after sorting to release objects
	// See https://github.com/jquery/sizzle/pull/225
	sortInput = null;

	return results;
};

/**
 * Utility function for retrieving the text value of an array of DOM nodes
 * @param {Array|Element} elem
 */
getText = Sizzle.getText = function( elem ) {
	var node,
		ret = "",
		i = 0,
		nodeType = elem.nodeType;

	if ( !nodeType ) {

		// If no nodeType, this is expected to be an array
		while ( ( node = elem[ i++ ] ) ) {

			// Do not traverse comment nodes
			ret += getText( node );
		}
	} else if ( nodeType === 1 || nodeType === 9 || nodeType === 11 ) {

		// Use textContent for elements
		// innerText usage removed for consistency of new lines (jQuery #11153)
		if ( typeof elem.textContent === "string" ) {
			return elem.textContent;
		} else {

			// Traverse its children
			for ( elem = elem.firstChild; elem; elem = elem.nextSibling ) {
				ret += getText( elem );
			}
		}
	} else if ( nodeType === 3 || nodeType === 4 ) {
		return elem.nodeValue;
	}

	// Do not include comment or processing instruction nodes

	return ret;
};

Expr = Sizzle.selectors = {

	// Can be adjusted by the user
	cacheLength: 50,

	createPseudo: markFunction,

	match: matchExpr,

	attrHandle: {},

	find: {},

	relative: {
		">": { dir: "parentNode", first: true },
		" ": { dir: "parentNode" },
		"+": { dir: "previousSibling", first: true },
		"~": { dir: "previousSibling" }
	},

	preFilter: {
		"ATTR": function( match ) {
			match[ 1 ] = match[ 1 ].replace( runescape, funescape );

			// Move the given value to match[3] whether quoted or unquoted
			match[ 3 ] = ( match[ 3 ] || match[ 4 ] ||
				match[ 5 ] || "" ).replace( runescape, funescape );

			if ( match[ 2 ] === "~=" ) {
				match[ 3 ] = " " + match[ 3 ] + " ";
			}

			return match.slice( 0, 4 );
		},

		"CHILD": function( match ) {

			/* matches from matchExpr["CHILD"]
				1 type (only|nth|...)
				2 what (child|of-type)
				3 argument (even|odd|\d*|\d*n([+-]\d+)?|...)
				4 xn-component of xn+y argument ([+-]?\d*n|)
				5 sign of xn-component
				6 x of xn-component
				7 sign of y-component
				8 y of y-component
			*/
			match[ 1 ] = match[ 1 ].toLowerCase();

			if ( match[ 1 ].slice( 0, 3 ) === "nth" ) {

				// nth-* requires argument
				if ( !match[ 3 ] ) {
					Sizzle.error( match[ 0 ] );
				}

				// numeric x and y parameters for Expr.filter.CHILD
				// remember that false/true cast respectively to 0/1
				match[ 4 ] = +( match[ 4 ] ?
					match[ 5 ] + ( match[ 6 ] || 1 ) :
					2 * ( match[ 3 ] === "even" || match[ 3 ] === "odd" ) );
				match[ 5 ] = +( ( match[ 7 ] + match[ 8 ] ) || match[ 3 ] === "odd" );

				// other types prohibit arguments
			} else if ( match[ 3 ] ) {
				Sizzle.error( match[ 0 ] );
			}

			return match;
		},

		"PSEUDO": function( match ) {
			var excess,
				unquoted = !match[ 6 ] && match[ 2 ];

			if ( matchExpr[ "CHILD" ].test( match[ 0 ] ) ) {
				return null;
			}

			// Accept quoted arguments as-is
			if ( match[ 3 ] ) {
				match[ 2 ] = match[ 4 ] || match[ 5 ] || "";

			// Strip excess characters from unquoted arguments
			} else if ( unquoted && rpseudo.test( unquoted ) &&

				// Get excess from tokenize (recursively)
				( excess = tokenize( unquoted, true ) ) &&

				// advance to the next closing parenthesis
				( excess = unquoted.indexOf( ")", unquoted.length - excess ) - unquoted.length ) ) {

				// excess is a negative index
				match[ 0 ] = match[ 0 ].slice( 0, excess );
				match[ 2 ] = unquoted.slice( 0, excess );
			}

			// Return only captures needed by the pseudo filter method (type and argument)
			return match.slice( 0, 3 );
		}
	},

	filter: {

		"TAG": function( nodeNameSelector ) {
			var nodeName = nodeNameSelector.replace( runescape, funescape ).toLowerCase();
			return nodeNameSelector === "*" ?
				function() {
					return true;
				} :
				function( elem ) {
					return elem.nodeName && elem.nodeName.toLowerCase() === nodeName;
				};
		},

		"CLASS": function( className ) {
			var pattern = classCache[ className + " " ];

			return pattern ||
				( pattern = new RegExp( "(^|" + whitespace +
					")" + className + "(" + whitespace + "|$)" ) ) && classCache(
						className, function( elem ) {
							return pattern.test(
								typeof elem.className === "string" && elem.className ||
								typeof elem.getAttribute !== "undefined" &&
									elem.getAttribute( "class" ) ||
								""
							);
				} );
		},

		"ATTR": function( name, operator, check ) {
			return function( elem ) {
				var result = Sizzle.attr( elem, name );

				if ( result == null ) {
					return operator === "!=";
				}
				if ( !operator ) {
					return true;
				}

				result += "";

				/* eslint-disable max-len */

				return operator === "=" ? result === check :
					operator === "!=" ? result !== check :
					operator === "^=" ? check && result.indexOf( check ) === 0 :
					operator === "*=" ? check && result.indexOf( check ) > -1 :
					operator === "$=" ? check && result.slice( -check.length ) === check :
					operator === "~=" ? ( " " + result.replace( rwhitespace, " " ) + " " ).indexOf( check ) > -1 :
					operator === "|=" ? result === check || result.slice( 0, check.length + 1 ) === check + "-" :
					false;
				/* eslint-enable max-len */

			};
		},

		"CHILD": function( type, what, _argument, first, last ) {
			var simple = type.slice( 0, 3 ) !== "nth",
				forward = type.slice( -4 ) !== "last",
				ofType = what === "of-type";

			return first === 1 && last === 0 ?

				// Shortcut for :nth-*(n)
				function( elem ) {
					return !!elem.parentNode;
				} :

				function( elem, _context, xml ) {
					var cache, uniqueCache, outerCache, node, nodeIndex, start,
						dir = simple !== forward ? "nextSibling" : "previousSibling",
						parent = elem.parentNode,
						name = ofType && elem.nodeName.toLowerCase(),
						useCache = !xml && !ofType,
						diff = false;

					if ( parent ) {

						// :(first|last|only)-(child|of-type)
						if ( simple ) {
							while ( dir ) {
								node = elem;
								while ( ( node = node[ dir ] ) ) {
									if ( ofType ?
										node.nodeName.toLowerCase() === name :
										node.nodeType === 1 ) {

										return false;
									}
								}

								// Reverse direction for :only-* (if we haven't yet done so)
								start = dir = type === "only" && !start && "nextSibling";
							}
							return true;
						}

						start = [ forward ? parent.firstChild : parent.lastChild ];

						// non-xml :nth-child(...) stores cache data on `parent`
						if ( forward && useCache ) {

							// Seek `elem` from a previously-cached index

							// ...in a gzip-friendly way
							node = parent;
							outerCache = node[ expando ] || ( node[ expando ] = {} );

							// Support: IE <9 only
							// Defend against cloned attroperties (jQuery gh-1709)
							uniqueCache = outerCache[ node.uniqueID ] ||
								( outerCache[ node.uniqueID ] = {} );

							cache = uniqueCache[ type ] || [];
							nodeIndex = cache[ 0 ] === dirruns && cache[ 1 ];
							diff = nodeIndex && cache[ 2 ];
							node = nodeIndex && parent.childNodes[ nodeIndex ];

							while ( ( node = ++nodeIndex && node && node[ dir ] ||

								// Fallback to seeking `elem` from the start
								( diff = nodeIndex = 0 ) || start.pop() ) ) {

								// When found, cache indexes on `parent` and break
								if ( node.nodeType === 1 && ++diff && node === elem ) {
									uniqueCache[ type ] = [ dirruns, nodeIndex, diff ];
									break;
								}
							}

						} else {

							// Use previously-cached element index if available
							if ( useCache ) {

								// ...in a gzip-friendly way
								node = elem;
								outerCache = node[ expando ] || ( node[ expando ] = {} );

								// Support: IE <9 only
								// Defend against cloned attroperties (jQuery gh-1709)
								uniqueCache = outerCache[ node.uniqueID ] ||
									( outerCache[ node.uniqueID ] = {} );

								cache = uniqueCache[ type ] || [];
								nodeIndex = cache[ 0 ] === dirruns && cache[ 1 ];
								diff = nodeIndex;
							}

							// xml :nth-child(...)
							// or :nth-last-child(...) or :nth(-last)?-of-type(...)
							if ( diff === false ) {

								// Use the same loop as above to seek `elem` from the start
								while ( ( node = ++nodeIndex && node && node[ dir ] ||
									( diff = nodeIndex = 0 ) || start.pop() ) ) {

									if ( ( ofType ?
										node.nodeName.toLowerCase() === name :
										node.nodeType === 1 ) &&
										++diff ) {

										// Cache the index of each encountered element
										if ( useCache ) {
											outerCache = node[ expando ] ||
												( node[ expando ] = {} );

											// Support: IE <9 only
											// Defend against cloned attroperties (jQuery gh-1709)
											uniqueCache = outerCache[ node.uniqueID ] ||
												( outerCache[ node.uniqueID ] = {} );

											uniqueCache[ type ] = [ dirruns, diff ];
										}

										if ( node === elem ) {
											break;
										}
									}
								}
							}
						}

						// Incorporate the offset, then check against cycle size
						diff -= last;
						return diff === first || ( diff % first === 0 && diff / first >= 0 );
					}
				};
		},

		"PSEUDO": function( pseudo, argument ) {

			// pseudo-class names are case-insensitive
			// http://www.w3.org/TR/selectors/#pseudo-classes
			// Prioritize by case sensitivity in case custom pseudos are added with uppercase letters
			// Remember that setFilters inherits from pseudos
			var args,
				fn = Expr.pseudos[ pseudo ] || Expr.setFilters[ pseudo.toLowerCase() ] ||
					Sizzle.error( "unsupported pseudo: " + pseudo );

			// The user may use createPseudo to indicate that
			// arguments are needed to create the filter function
			// just as Sizzle does
			if ( fn[ expando ] ) {
				return fn( argument );
			}

			// But maintain support for old signatures
			if ( fn.length > 1 ) {
				args = [ pseudo, pseudo, "", argument ];
				return Expr.setFilters.hasOwnProperty( pseudo.toLowerCase() ) ?
					markFunction( function( seed, matches ) {
						var idx,
							matched = fn( seed, argument ),
							i = matched.length;
						while ( i-- ) {
							idx = indexOf( seed, matched[ i ] );
							seed[ idx ] = !( matches[ idx ] = matched[ i ] );
						}
					} ) :
					function( elem ) {
						return fn( elem, 0, args );
					};
			}

			return fn;
		}
	},

	pseudos: {

		// Potentially complex pseudos
		"not": markFunction( function( selector ) {

			// Trim the selector passed to compile
			// to avoid treating leading and trailing
			// spaces as combinators
			var input = [],
				results = [],
				matcher = compile( selector.replace( rtrim, "$1" ) );

			return matcher[ expando ] ?
				markFunction( function( seed, matches, _context, xml ) {
					var elem,
						unmatched = matcher( seed, null, xml, [] ),
						i = seed.length;

					// Match elements unmatched by `matcher`
					while ( i-- ) {
						if ( ( elem = unmatched[ i ] ) ) {
							seed[ i ] = !( matches[ i ] = elem );
						}
					}
				} ) :
				function( elem, _context, xml ) {
					input[ 0 ] = elem;
					matcher( input, null, xml, results );

					// Don't keep the element (issue #299)
					input[ 0 ] = null;
					return !results.pop();
				};
		} ),

		"has": markFunction( function( selector ) {
			return function( elem ) {
				return Sizzle( selector, elem ).length > 0;
			};
		} ),

		"contains": markFunction( function( text ) {
			text = text.replace( runescape, funescape );
			return function( elem ) {
				return ( elem.textContent || getText( elem ) ).indexOf( text ) > -1;
			};
		} ),

		// "Whether an element is represented by a :lang() selector
		// is based solely on the element's language value
		// being equal to the identifier C,
		// or beginning with the identifier C immediately followed by "-".
		// The matching of C against the element's language value is performed case-insensitively.
		// The identifier C does not have to be a valid language name."
		// http://www.w3.org/TR/selectors/#lang-pseudo
		"lang": markFunction( function( lang ) {

			// lang value must be a valid identifier
			if ( !ridentifier.test( lang || "" ) ) {
				Sizzle.error( "unsupported lang: " + lang );
			}
			lang = lang.replace( runescape, funescape ).toLowerCase();
			return function( elem ) {
				var elemLang;
				do {
					if ( ( elemLang = documentIsHTML ?
						elem.lang :
						elem.getAttribute( "xml:lang" ) || elem.getAttribute( "lang" ) ) ) {

						elemLang = elemLang.toLowerCase();
						return elemLang === lang || elemLang.indexOf( lang + "-" ) === 0;
					}
				} while ( ( elem = elem.parentNode ) && elem.nodeType === 1 );
				return false;
			};
		} ),

		// Miscellaneous
		"target": function( elem ) {
			var hash = window.location && window.location.hash;
			return hash && hash.slice( 1 ) === elem.id;
		},

		"root": function( elem ) {
			return elem === docElem;
		},

		"focus": function( elem ) {
			return elem === document.activeElement &&
				( !document.hasFocus || document.hasFocus() ) &&
				!!( elem.type || elem.href || ~elem.tabIndex );
		},

		// Boolean properties
		"enabled": createDisabledPseudo( false ),
		"disabled": createDisabledPseudo( true ),

		"checked": function( elem ) {

			// In CSS3, :checked should return both checked and selected elements
			// http://www.w3.org/TR/2011/REC-css3-selectors-20110929/#checked
			var nodeName = elem.nodeName.toLowerCase();
			return ( nodeName === "input" && !!elem.checked ) ||
				( nodeName === "option" && !!elem.selected );
		},

		"selected": function( elem ) {

			// Accessing this property makes selected-by-default
			// options in Safari work properly
			if ( elem.parentNode ) {
				// eslint-disable-next-line no-unused-expressions
				elem.parentNode.selectedIndex;
			}

			return elem.selected === true;
		},

		// Contents
		"empty": function( elem ) {

			// http://www.w3.org/TR/selectors/#empty-pseudo
			// :empty is negated by element (1) or content nodes (text: 3; cdata: 4; entity ref: 5),
			//   but not by others (comment: 8; processing instruction: 7; etc.)
			// nodeType < 6 works because attributes (2) do not appear as children
			for ( elem = elem.firstChild; elem; elem = elem.nextSibling ) {
				if ( elem.nodeType < 6 ) {
					return false;
				}
			}
			return true;
		},

		"parent": function( elem ) {
			return !Expr.pseudos[ "empty" ]( elem );
		},

		// Element/input types
		"header": function( elem ) {
			return rheader.test( elem.nodeName );
		},

		"input": function( elem ) {
			return rinputs.test( elem.nodeName );
		},

		"button": function( elem ) {
			var name = elem.nodeName.toLowerCase();
			return name === "input" && elem.type === "button" || name === "button";
		},

		"text": function( elem ) {
			var attr;
			return elem.nodeName.toLowerCase() === "input" &&
				elem.type === "text" &&

				// Support: IE<8
				// New HTML5 attribute values (e.g., "search") appear with elem.type === "text"
				( ( attr = elem.getAttribute( "type" ) ) == null ||
					attr.toLowerCase() === "text" );
		},

		// Position-in-collection
		"first": createPositionalPseudo( function() {
			return [ 0 ];
		} ),

		"last": createPositionalPseudo( function( _matchIndexes, length ) {
			return [ length - 1 ];
		} ),

		"eq": createPositionalPseudo( function( _matchIndexes, length, argument ) {
			return [ argument < 0 ? argument + length : argument ];
		} ),

		"even": createPositionalPseudo( function( matchIndexes, length ) {
			var i = 0;
			for ( ; i < length; i += 2 ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"odd": createPositionalPseudo( function( matchIndexes, length ) {
			var i = 1;
			for ( ; i < length; i += 2 ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"lt": createPositionalPseudo( function( matchIndexes, length, argument ) {
			var i = argument < 0 ?
				argument + length :
				argument > length ?
					length :
					argument;
			for ( ; --i >= 0; ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} ),

		"gt": createPositionalPseudo( function( matchIndexes, length, argument ) {
			var i = argument < 0 ? argument + length : argument;
			for ( ; ++i < length; ) {
				matchIndexes.push( i );
			}
			return matchIndexes;
		} )
	}
};

Expr.pseudos[ "nth" ] = Expr.pseudos[ "eq" ];

// Add button/input type pseudos
for ( i in { radio: true, checkbox: true, file: true, password: true, image: true } ) {
	Expr.pseudos[ i ] = createInputPseudo( i );
}
for ( i in { submit: true, reset: true } ) {
	Expr.pseudos[ i ] = createButtonPseudo( i );
}

// Easy API for creating new setFilters
function setFilters() {}
setFilters.prototype = Expr.filters = Expr.pseudos;
Expr.setFilters = new setFilters();

tokenize = Sizzle.tokenize = function( selector, parseOnly ) {
	var matched, match, tokens, type,
		soFar, groups, preFilters,
		cached = tokenCache[ selector + " " ];

	if ( cached ) {
		return parseOnly ? 0 : cached.slice( 0 );
	}

	soFar = selector;
	groups = [];
	preFilters = Expr.preFilter;

	while ( soFar ) {

		// Comma and first run
		if ( !matched || ( match = rcomma.exec( soFar ) ) ) {
			if ( match ) {

				// Don't consume trailing commas as valid
				soFar = soFar.slice( match[ 0 ].length ) || soFar;
			}
			groups.push( ( tokens = [] ) );
		}

		matched = false;

		// Combinators
		if ( ( match = rcombinators.exec( soFar ) ) ) {
			matched = match.shift();
			tokens.push( {
				value: matched,

				// Cast descendant combinators to space
				type: match[ 0 ].replace( rtrim, " " )
			} );
			soFar = soFar.slice( matched.length );
		}

		// Filters
		for ( type in Expr.filter ) {
			if ( ( match = matchExpr[ type ].exec( soFar ) ) && ( !preFilters[ type ] ||
				( match = preFilters[ type ]( match ) ) ) ) {
				matched = match.shift();
				tokens.push( {
					value: matched,
					type: type,
					matches: match
				} );
				soFar = soFar.slice( matched.length );
			}
		}

		if ( !matched ) {
			break;
		}
	}

	// Return the length of the invalid excess
	// if we're just parsing
	// Otherwise, throw an error or return tokens
	return parseOnly ?
		soFar.length :
		soFar ?
			Sizzle.error( selector ) :

			// Cache the tokens
			tokenCache( selector, groups ).slice( 0 );
};

function toSelector( tokens ) {
	var i = 0,
		len = tokens.length,
		selector = "";
	for ( ; i < len; i++ ) {
		selector += tokens[ i ].value;
	}
	return selector;
}

function addCombinator( matcher, combinator, base ) {
	var dir = combinator.dir,
		skip = combinator.next,
		key = skip || dir,
		checkNonElements = base && key === "parentNode",
		doneName = done++;

	return combinator.first ?

		// Check against closest ancestor/preceding element
		function( elem, context, xml ) {
			while ( ( elem = elem[ dir ] ) ) {
				if ( elem.nodeType === 1 || checkNonElements ) {
					return matcher( elem, context, xml );
				}
			}
			return false;
		} :

		// Check against all ancestor/preceding elements
		function( elem, context, xml ) {
			var oldCache, uniqueCache, outerCache,
				newCache = [ dirruns, doneName ];

			// We can't set arbitrary data on XML nodes, so they don't benefit from combinator caching
			if ( xml ) {
				while ( ( elem = elem[ dir ] ) ) {
					if ( elem.nodeType === 1 || checkNonElements ) {
						if ( matcher( elem, context, xml ) ) {
							return true;
						}
					}
				}
			} else {
				while ( ( elem = elem[ dir ] ) ) {
					if ( elem.nodeType === 1 || checkNonElements ) {
						outerCache = elem[ expando ] || ( elem[ expando ] = {} );

						// Support: IE <9 only
						// Defend against cloned attroperties (jQuery gh-1709)
						uniqueCache = outerCache[ elem.uniqueID ] ||
							( outerCache[ elem.uniqueID ] = {} );

						if ( skip && skip === elem.nodeName.toLowerCase() ) {
							elem = elem[ dir ] || elem;
						} else if ( ( oldCache = uniqueCache[ key ] ) &&
							oldCache[ 0 ] === dirruns && oldCache[ 1 ] === doneName ) {

							// Assign to newCache so results back-propagate to previous elements
							return ( newCache[ 2 ] = oldCache[ 2 ] );
						} else {

							// Reuse newcache so results back-propagate to previous elements
							uniqueCache[ key ] = newCache;

							// A match means we're done; a fail means we have to keep checking
							if ( ( newCache[ 2 ] = matcher( elem, context, xml ) ) ) {
								return true;
							}
						}
					}
				}
			}
			return false;
		};
}

function elementMatcher( matchers ) {
	return matchers.length > 1 ?
		function( elem, context, xml ) {
			var i = matchers.length;
			while ( i-- ) {
				if ( !matchers[ i ]( elem, context, xml ) ) {
					return false;
				}
			}
			return true;
		} :
		matchers[ 0 ];
}

function multipleContexts( selector, contexts, results ) {
	var i = 0,
		len = contexts.length;
	for ( ; i < len; i++ ) {
		Sizzle( selector, contexts[ i ], results );
	}
	return results;
}

function condense( unmatched, map, filter, context, xml ) {
	var elem,
		newUnmatched = [],
		i = 0,
		len = unmatched.length,
		mapped = map != null;

	for ( ; i < len; i++ ) {
		if ( ( elem = unmatched[ i ] ) ) {
			if ( !filter || filter( elem, context, xml ) ) {
				newUnmatched.push( elem );
				if ( mapped ) {
					map.push( i );
				}
			}
		}
	}

	return newUnmatched;
}

function setMatcher( preFilter, selector, matcher, postFilter, postFinder, postSelector ) {
	if ( postFilter && !postFilter[ expando ] ) {
		postFilter = setMatcher( postFilter );
	}
	if ( postFinder && !postFinder[ expando ] ) {
		postFinder = setMatcher( postFinder, postSelector );
	}
	return markFunction( function( seed, results, context, xml ) {
		var temp, i, elem,
			preMap = [],
			postMap = [],
			preexisting = results.length,

			// Get initial elements from seed or context
			elems = seed || multipleContexts(
				selector || "*",
				context.nodeType ? [ context ] : context,
				[]
			),

			// Prefilter to get matcher input, preserving a map for seed-results synchronization
			matcherIn = preFilter && ( seed || !selector ) ?
				condense( elems, preMap, preFilter, context, xml ) :
				elems,

			matcherOut = matcher ?

				// If we have a postFinder, or filtered seed, or non-seed postFilter or preexisting results,
				postFinder || ( seed ? preFilter : preexisting || postFilter ) ?

					// ...intermediate processing is necessary
					[] :

					// ...otherwise use results directly
					results :
				matcherIn;

		// Find primary matches
		if ( matcher ) {
			matcher( matcherIn, matcherOut, context, xml );
		}

		// Apply postFilter
		if ( postFilter ) {
			temp = condense( matcherOut, postMap );
			postFilter( temp, [], context, xml );

			// Un-match failing elements by moving them back to matcherIn
			i = temp.length;
			while ( i-- ) {
				if ( ( elem = temp[ i ] ) ) {
					matcherOut[ postMap[ i ] ] = !( matcherIn[ postMap[ i ] ] = elem );
				}
			}
		}

		if ( seed ) {
			if ( postFinder || preFilter ) {
				if ( postFinder ) {

					// Get the final matcherOut by condensing this intermediate into postFinder contexts
					temp = [];
					i = matcherOut.length;
					while ( i-- ) {
						if ( ( elem = matcherOut[ i ] ) ) {

							// Restore matcherIn since elem is not yet a final match
							temp.push( ( matcherIn[ i ] = elem ) );
						}
					}
					postFinder( null, ( matcherOut = [] ), temp, xml );
				}

				// Move matched elements from seed to results to keep them synchronized
				i = matcherOut.length;
				while ( i-- ) {
					if ( ( elem = matcherOut[ i ] ) &&
						( temp = postFinder ? indexOf( seed, elem ) : preMap[ i ] ) > -1 ) {

						seed[ temp ] = !( results[ temp ] = elem );
					}
				}
			}

		// Add elements to results, through postFinder if defined
		} else {
			matcherOut = condense(
				matcherOut === results ?
					matcherOut.splice( preexisting, matcherOut.length ) :
					matcherOut
			);
			if ( postFinder ) {
				postFinder( null, results, matcherOut, xml );
			} else {
				push.apply( results, matcherOut );
			}
		}
	} );
}

function matcherFromTokens( tokens ) {
	var checkContext, matcher, j,
		len = tokens.length,
		leadingRelative = Expr.relative[ tokens[ 0 ].type ],
		implicitRelative = leadingRelative || Expr.relative[ " " ],
		i = leadingRelative ? 1 : 0,

		// The foundational matcher ensures that elements are reachable from top-level context(s)
		matchContext = addCombinator( function( elem ) {
			return elem === checkContext;
		}, implicitRelative, true ),
		matchAnyContext = addCombinator( function( elem ) {
			return indexOf( checkContext, elem ) > -1;
		}, implicitRelative, true ),
		matchers = [ function( elem, context, xml ) {
			var ret = ( !leadingRelative && ( xml || context !== outermostContext ) ) || (
				( checkContext = context ).nodeType ?
					matchContext( elem, context, xml ) :
					matchAnyContext( elem, context, xml ) );

			// Avoid hanging onto element (issue #299)
			checkContext = null;
			return ret;
		} ];

	for ( ; i < len; i++ ) {
		if ( ( matcher = Expr.relative[ tokens[ i ].type ] ) ) {
			matchers = [ addCombinator( elementMatcher( matchers ), matcher ) ];
		} else {
			matcher = Expr.filter[ tokens[ i ].type ].apply( null, tokens[ i ].matches );

			// Return special upon seeing a positional matcher
			if ( matcher[ expando ] ) {

				// Find the next relative operator (if any) for proper handling
				j = ++i;
				for ( ; j < len; j++ ) {
					if ( Expr.relative[ tokens[ j ].type ] ) {
						break;
					}
				}
				return setMatcher(
					i > 1 && elementMatcher( matchers ),
					i > 1 && toSelector(

					// If the preceding token was a descendant combinator, insert an implicit any-element `*`
					tokens
						.slice( 0, i - 1 )
						.concat( { value: tokens[ i - 2 ].type === " " ? "*" : "" } )
					).replace( rtrim, "$1" ),
					matcher,
					i < j && matcherFromTokens( tokens.slice( i, j ) ),
					j < len && matcherFromTokens( ( tokens = tokens.slice( j ) ) ),
					j < len && toSelector( tokens )
				);
			}
			matchers.push( matcher );
		}
	}

	return elementMatcher( matchers );
}

function matcherFromGroupMatchers( elementMatchers, setMatchers ) {
	var bySet = setMatchers.length > 0,
		byElement = elementMatchers.length > 0,
		superMatcher = function( seed, context, xml, results, outermost ) {
			var elem, j, matcher,
				matchedCount = 0,
				i = "0",
				unmatched = seed && [],
				setMatched = [],
				contextBackup = outermostContext,

				// We must always have either seed elements or outermost context
				elems = seed || byElement && Expr.find[ "TAG" ]( "*", outermost ),

				// Use integer dirruns iff this is the outermost matcher
				dirrunsUnique = ( dirruns += contextBackup == null ? 1 : Math.random() || 0.1 ),
				len = elems.length;

			if ( outermost ) {

				// Support: IE 11+, Edge 17 - 18+
				// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
				// two documents; shallow comparisons work.
				// eslint-disable-next-line eqeqeq
				outermostContext = context == document || context || outermost;
			}

			// Add elements passing elementMatchers directly to results
			// Support: IE<9, Safari
			// Tolerate NodeList properties (IE: "length"; Safari: <number>) matching elements by id
			for ( ; i !== len && ( elem = elems[ i ] ) != null; i++ ) {
				if ( byElement && elem ) {
					j = 0;

					// Support: IE 11+, Edge 17 - 18+
					// IE/Edge sometimes throw a "Permission denied" error when strict-comparing
					// two documents; shallow comparisons work.
					// eslint-disable-next-line eqeqeq
					if ( !context && elem.ownerDocument != document ) {
						setDocument( elem );
						xml = !documentIsHTML;
					}
					while ( ( matcher = elementMatchers[ j++ ] ) ) {
						if ( matcher( elem, context || document, xml ) ) {
							results.push( elem );
							break;
						}
					}
					if ( outermost ) {
						dirruns = dirrunsUnique;
					}
				}

				// Track unmatched elements for set filters
				if ( bySet ) {

					// They will have gone through all possible matchers
					if ( ( elem = !matcher && elem ) ) {
						matchedCount--;
					}

					// Lengthen the array for every element, matched or not
					if ( seed ) {
						unmatched.push( elem );
					}
				}
			}

			// `i` is now the count of elements visited above, and adding it to `matchedCount`
			// makes the latter nonnegative.
			matchedCount += i;

			// Apply set filters to unmatched elements
			// NOTE: This can be skipped if there are no unmatched elements (i.e., `matchedCount`
			// equals `i`), unless we didn't visit _any_ elements in the above loop because we have
			// no element matchers and no seed.
			// Incrementing an initially-string "0" `i` allows `i` to remain a string only in that
			// case, which will result in a "00" `matchedCount` that differs from `i` but is also
			// numerically zero.
			if ( bySet && i !== matchedCount ) {
				j = 0;
				while ( ( matcher = setMatchers[ j++ ] ) ) {
					matcher( unmatched, setMatched, context, xml );
				}

				if ( seed ) {

					// Reintegrate element matches to eliminate the need for sorting
					if ( matchedCount > 0 ) {
						while ( i-- ) {
							if ( !( unmatched[ i ] || setMatched[ i ] ) ) {
								setMatched[ i ] = pop.call( results );
							}
						}
					}

					// Discard index placeholder values to get only actual matches
					setMatched = condense( setMatched );
				}

				// Add matches to results
				push.apply( results, setMatched );

				// Seedless set matches succeeding multiple successful matchers stipulate sorting
				if ( outermost && !seed && setMatched.length > 0 &&
					( matchedCount + setMatchers.length ) > 1 ) {

					Sizzle.uniqueSort( results );
				}
			}

			// Override manipulation of globals by nested matchers
			if ( outermost ) {
				dirruns = dirrunsUnique;
				outermostContext = contextBackup;
			}

			return unmatched;
		};

	return bySet ?
		markFunction( superMatcher ) :
		superMatcher;
}

compile = Sizzle.compile = function( selector, match /* Internal Use Only */ ) {
	var i,
		setMatchers = [],
		elementMatchers = [],
		cached = compilerCache[ selector + " " ];

	if ( !cached ) {

		// Generate a function of recursive functions that can be used to check each element
		if ( !match ) {
			match = tokenize( selector );
		}
		i = match.length;
		while ( i-- ) {
			cached = matcherFromTokens( match[ i ] );
			if ( cached[ expando ] ) {
				setMatchers.push( cached );
			} else {
				elementMatchers.push( cached );
			}
		}

		// Cache the compiled function
		cached = compilerCache(
			selector,
			matcherFromGroupMatchers( elementMatchers, setMatchers )
		);

		// Save selector and tokenization
		cached.selector = selector;
	}
	return cached;
};

/**
 * A low-level selection function that works with Sizzle's compiled
 *  selector functions
 * @param {String|Function} selector A selector or a pre-compiled
 *  selector function built with Sizzle.compile
 * @param {Element} context
 * @param {Array} [results]
 * @param {Array} [seed] A set of elements to match against
 */
select = Sizzle.select = function( selector, context, results, seed ) {
	var i, tokens, token, type, find,
		compiled = typeof selector === "function" && selector,
		match = !seed && tokenize( ( selector = compiled.selector || selector ) );

	results = results || [];

	// Try to minimize operations if there is only one selector in the list and no seed
	// (the latter of which guarantees us context)
	if ( match.length === 1 ) {

		// Reduce context if the leading compound selector is an ID
		tokens = match[ 0 ] = match[ 0 ].slice( 0 );
		if ( tokens.length > 2 && ( token = tokens[ 0 ] ).type === "ID" &&
			context.nodeType === 9 && documentIsHTML && Expr.relative[ tokens[ 1 ].type ] ) {

			context = ( Expr.find[ "ID" ]( token.matches[ 0 ]
				.replace( runescape, funescape ), context ) || [] )[ 0 ];
			if ( !context ) {
				return results;

			// Precompiled matchers will still verify ancestry, so step up a level
			} else if ( compiled ) {
				context = context.parentNode;
			}

			selector = selector.slice( tokens.shift().value.length );
		}

		// Fetch a seed set for right-to-left matching
		i = matchExpr[ "needsContext" ].test( selector ) ? 0 : tokens.length;
		while ( i-- ) {
			token = tokens[ i ];

			// Abort if we hit a combinator
			if ( Expr.relative[ ( type = token.type ) ] ) {
				break;
			}
			if ( ( find = Expr.find[ type ] ) ) {

				// Search, expanding context for leading sibling combinators
				if ( ( seed = find(
					token.matches[ 0 ].replace( runescape, funescape ),
					rsibling.test( tokens[ 0 ].type ) && testContext( context.parentNode ) ||
						context
				) ) ) {

					// If seed is empty or no tokens remain, we can return early
					tokens.splice( i, 1 );
					selector = seed.length && toSelector( tokens );
					if ( !selector ) {
						push.apply( results, seed );
						return results;
					}

					break;
				}
			}
		}
	}

	// Compile and execute a filtering function if one is not provided
	// Provide `match` to avoid retokenization if we modified the selector above
	( compiled || compile( selector, match ) )(
		seed,
		context,
		!documentIsHTML,
		results,
		!context || rsibling.test( selector ) && testContext( context.parentNode ) || context
	);
	return results;
};

// One-time assignments

// Sort stability
support.sortStable = expando.split( "" ).sort( sortOrder ).join( "" ) === expando;

// Support: Chrome 14-35+
// Always assume duplicates if they aren't passed to the comparison function
support.detectDuplicates = !!hasDuplicate;

// Initialize against the default document
setDocument();

// Support: Webkit<537.32 - Safari 6.0.3/Chrome 25 (fixed in Chrome 27)
// Detached nodes confoundingly follow *each other*
support.sortDetached = assert( function( el ) {

	// Should return 1, but returns 4 (following)
	return el.compareDocumentPosition( document.createElement( "fieldset" ) ) & 1;
} );

// Support: IE<8
// Prevent attribute/property "interpolation"
// https://msdn.microsoft.com/en-us/library/ms536429%28VS.85%29.aspx
if ( !assert( function( el ) {
	el.innerHTML = "<a href='#'></a>";
	return el.firstChild.getAttribute( "href" ) === "#";
} ) ) {
	addHandle( "type|href|height|width", function( elem, name, isXML ) {
		if ( !isXML ) {
			return elem.getAttribute( name, name.toLowerCase() === "type" ? 1 : 2 );
		}
	} );
}

// Support: IE<9
// Use defaultValue in place of getAttribute("value")
if ( !support.attributes || !assert( function( el ) {
	el.innerHTML = "<input/>";
	el.firstChild.setAttribute( "value", "" );
	return el.firstChild.getAttribute( "value" ) === "";
} ) ) {
	addHandle( "value", function( elem, _name, isXML ) {
		if ( !isXML && elem.nodeName.toLowerCase() === "input" ) {
			return elem.defaultValue;
		}
	} );
}

// Support: IE<9
// Use getAttributeNode to fetch booleans when getAttribute lies
if ( !assert( function( el ) {
	return el.getAttribute( "disabled" ) == null;
} ) ) {
	addHandle( booleans, function( elem, name, isXML ) {
		var val;
		if ( !isXML ) {
			return elem[ name ] === true ? name.toLowerCase() :
				( val = elem.getAttributeNode( name ) ) && val.specified ?
					val.value :
					null;
		}
	} );
}

return Sizzle;

} )( window );



jQuery.find = Sizzle;
jQuery.expr = Sizzle.selectors;

// Deprecated
jQuery.expr[ ":" ] = jQuery.expr.pseudos;
jQuery.uniqueSort = jQuery.unique = Sizzle.uniqueSort;
jQuery.text = Sizzle.getText;
jQuery.isXMLDoc = Sizzle.isXML;
jQuery.contains = Sizzle.contains;
jQuery.escapeSelector = Sizzle.escape;




var dir = function( elem, dir, until ) {
	var matched = [],
		truncate = until !== undefined;

	while ( ( elem = elem[ dir ] ) && elem.nodeType !== 9 ) {
		if ( elem.nodeType === 1 ) {
			if ( truncate && jQuery( elem ).is( until ) ) {
				break;
			}
			matched.push( elem );
		}
	}
	return matched;
};


var siblings = function( n, elem ) {
	var matched = [];

	for ( ; n; n = n.nextSibling ) {
		if ( n.nodeType === 1 && n !== elem ) {
			matched.push( n );
		}
	}

	return matched;
};


var rneedsContext = jQuery.expr.match.needsContext;



function nodeName( elem, name ) {

  return elem.nodeName && elem.nodeName.toLowerCase() === name.toLowerCase();

};
var rsingleTag = ( /^<([a-z][^\/\0>:\x20\t\r\n\f]*)[\x20\t\r\n\f]*\/?>(?:<\/\1>|)$/i );



// Implement the identical functionality for filter and not
function winnow( elements, qualifier, not ) {
	if ( isFunction( qualifier ) ) {
		return jQuery.grep( elements, function( elem, i ) {
			return !!qualifier.call( elem, i, elem ) !== not;
		} );
	}

	// Single element
	if ( qualifier.nodeType ) {
		return jQuery.grep( elements, function( elem ) {
			return ( elem === qualifier ) !== not;
		} );
	}

	// Arraylike of elements (jQuery, arguments, Array)
	if ( typeof qualifier !== "string" ) {
		return jQuery.grep( elements, function( elem ) {
			return ( indexOf.call( qualifier, elem ) > -1 ) !== not;
		} );
	}

	// Filtered directly for both simple and complex selectors
	return jQuery.filter( qualifier, elements, not );
}

jQuery.filter = function( expr, elems, not ) {
	var elem = elems[ 0 ];

	if ( not ) {
		expr = ":not(" + expr + ")";
	}

	if ( elems.length === 1 && elem.nodeType === 1 ) {
		return jQuery.find.matchesSelector( elem, expr ) ? [ elem ] : [];
	}

	return jQuery.find.matches( expr, jQuery.grep( elems, function( elem ) {
		return elem.nodeType === 1;
	} ) );
};

jQuery.fn.extend( {
	find: function( selector ) {
		var i, ret,
			len = this.length,
			self = this;

		if ( typeof selector !== "string" ) {
			return this.pushStack( jQuery( selector ).filter( function() {
				for ( i = 0; i < len; i++ ) {
					if ( jQuery.contains( self[ i ], this ) ) {
						return true;
					}
				}
			} ) );
		}

		ret = this.pushStack( [] );

		for ( i = 0; i < len; i++ ) {
			jQuery.find( selector, self[ i ], ret );
		}

		return len > 1 ? jQuery.uniqueSort( ret ) : ret;
	},
	filter: function( selector ) {
		return this.pushStack( winnow( this, selector || [], false ) );
	},
	not: function( selector ) {
		return this.pushStack( winnow( this, selector || [], true ) );
	},
	is: function( selector ) {
		return !!winnow(
			this,

			// If this is a positional/relative selector, check membership in the returned set
			// so $("p:first").is("p:last") won't return true for a doc with two "p".
			typeof selector === "string" && rneedsContext.test( selector ) ?
				jQuery( selector ) :
				selector || [],
			false
		).length;
	}
} );


// Initialize a jQuery object


// A central reference to the root jQuery(document)
var rootjQuery,

	// A simple way to check for HTML strings
	// Prioritize #id over <tag> to avoid XSS via location.hash (#9521)
	// Strict HTML recognition (#11290: must start with <)
	// Shortcut simple #id case for speed
	rquickExpr = /^(?:\s*(<[\w\W]+>)[^>]*|#([\w-]+))$/,

	init = jQuery.fn.init = function( selector, context, root ) {
		var match, elem;

		// HANDLE: $(""), $(null), $(undefined), $(false)
		if ( !selector ) {
			return this;
		}

		// Method init() accepts an alternate rootjQuery
		// so migrate can support jQuery.sub (gh-2101)
		root = root || rootjQuery;

		// Handle HTML strings
		if ( typeof selector === "string" ) {
			if ( selector[ 0 ] === "<" &&
				selector[ selector.length - 1 ] === ">" &&
				selector.length >= 3 ) {

				// Assume that strings that start and end with <> are HTML and skip the regex check
				match = [ null, selector, null ];

			} else {
				match = rquickExpr.exec( selector );
			}

			// Match html or make sure no context is specified for #id
			if ( match && ( match[ 1 ] || !context ) ) {

				// HANDLE: $(html) -> $(array)
				if ( match[ 1 ] ) {
					context = context instanceof jQuery ? context[ 0 ] : context;

					// Option to run scripts is true for back-compat
					// Intentionally let the error be thrown if parseHTML is not present
					jQuery.merge( this, jQuery.parseHTML(
						match[ 1 ],
						context && context.nodeType ? context.ownerDocument || context : document,
						true
					) );

					// HANDLE: $(html, props)
					if ( rsingleTag.test( match[ 1 ] ) && jQuery.isPlainObject( context ) ) {
						for ( match in context ) {

							// Properties of context are called as methods if possible
							if ( isFunction( this[ match ] ) ) {
								this[ match ]( context[ match ] );

							// ...and otherwise set as attributes
							} else {
								this.attr( match, context[ match ] );
							}
						}
					}

					return this;

				// HANDLE: $(#id)
				} else {
					elem = document.getElementById( match[ 2 ] );

					if ( elem ) {

						// Inject the element directly into the jQuery object
						this[ 0 ] = elem;
						this.length = 1;
					}
					return this;
				}

			// HANDLE: $(expr, $(...))
			} else if ( !context || context.jquery ) {
				return ( context || root ).find( selector );

			// HANDLE: $(expr, context)
			// (which is just equivalent to: $(context).find(expr)
			} else {
				return this.constructor( context ).find( selector );
			}

		// HANDLE: $(DOMElement)
		} else if ( selector.nodeType ) {
			this[ 0 ] = selector;
			this.length = 1;
			return this;

		// HANDLE: $(function)
		// Shortcut for document ready
		} else if ( isFunction( selector ) ) {
			return root.ready !== undefined ?
				root.ready( selector ) :

				// Execute immediately if ready is not present
				selector( jQuery );
		}

		return jQuery.makeArray( selector, this );
	};

// Give the init function the jQuery prototype for later instantiation
init.prototype = jQuery.fn;

// Initialize central reference
rootjQuery = jQuery( document );


var rparentsprev = /^(?:parents|prev(?:Until|All))/,

	// Methods guaranteed to produce a unique set when starting from a unique set
	guaranteedUnique = {
		children: true,
		contents: true,
		next: true,
		prev: true
	};

jQuery.fn.extend( {
	has: function( target ) {
		var targets = jQuery( target, this ),
			l = targets.length;

		return this.filter( function() {
			var i = 0;
			for ( ; i < l; i++ ) {
				if ( jQuery.contains( this, targets[ i ] ) ) {
					return true;
				}
			}
		} );
	},

	closest: function( selectors, context ) {
		var cur,
			i = 0,
			l = this.length,
			matched = [],
			targets = typeof selectors !== "string" && jQuery( selectors );

		// Positional selectors never match, since there's no _selection_ context
		if ( !rneedsContext.test( selectors ) ) {
			for ( ; i < l; i++ ) {
				for ( cur = this[ i ]; cur && cur !== context; cur = cur.parentNode ) {

					// Always skip document fragments
					if ( cur.nodeType < 11 && ( targets ?
						targets.index( cur ) > -1 :

						// Don't pass non-elements to Sizzle
						cur.nodeType === 1 &&
							jQuery.find.matchesSelector( cur, selectors ) ) ) {

						matched.push( cur );
						break;
					}
				}
			}
		}

		return this.pushStack( matched.length > 1 ? jQuery.uniqueSort( matched ) : matched );
	},

	// Determine the position of an element within the set
	index: function( elem ) {

		// No argument, return index in parent
		if ( !elem ) {
			return ( this[ 0 ] && this[ 0 ].parentNode ) ? this.first().prevAll().length : -1;
		}

		// Index in selector
		if ( typeof elem === "string" ) {
			return indexOf.call( jQuery( elem ), this[ 0 ] );
		}

		// Locate the position of the desired element
		return indexOf.call( this,

			// If it receives a jQuery object, the first element is used
			elem.jquery ? elem[ 0 ] : elem
		);
	},

	add: function( selector, context ) {
		return this.pushStack(
			jQuery.uniqueSort(
				jQuery.merge( this.get(), jQuery( selector, context ) )
			)
		);
	},

	addBack: function( selector ) {
		return this.add( selector == null ?
			this.prevObject : this.prevObject.filter( selector )
		);
	}
} );

function sibling( cur, dir ) {
	while ( ( cur = cur[ dir ] ) && cur.nodeType !== 1 ) {}
	return cur;
}

jQuery.each( {
	parent: function( elem ) {
		var parent = elem.parentNode;
		return parent && parent.nodeType !== 11 ? parent : null;
	},
	parents: function( elem ) {
		return dir( elem, "parentNode" );
	},
	parentsUntil: function( elem, _i, until ) {
		return dir( elem, "parentNode", until );
	},
	next: function( elem ) {
		return sibling( elem, "nextSibling" );
	},
	prev: function( elem ) {
		return sibling( elem, "previousSibling" );
	},
	nextAll: function( elem ) {
		return dir( elem, "nextSibling" );
	},
	prevAll: function( elem ) {
		return dir( elem, "previousSibling" );
	},
	nextUntil: function( elem, _i, until ) {
		return dir( elem, "nextSibling", until );
	},
	prevUntil: function( elem, _i, until ) {
		return dir( elem, "previousSibling", until );
	},
	siblings: function( elem ) {
		return siblings( ( elem.parentNode || {} ).firstChild, elem );
	},
	children: function( elem ) {
		return siblings( elem.firstChild );
	},
	contents: function( elem ) {
		if ( elem.contentDocument != null &&

			// Support: IE 11+
			// <object> elements with no `data` attribute has an object
			// `contentDocument` with a `null` prototype.
			getProto( elem.contentDocument ) ) {

			return elem.contentDocument;
		}

		// Support: IE 9 - 11 only, iOS 7 only, Android Browser <=4.3 only
		// Treat the template element as a regular one in browsers that
		// don't support it.
		if ( nodeName( elem, "template" ) ) {
			elem = elem.content || elem;
		}

		return jQuery.merge( [], elem.childNodes );
	}
}, function( name, fn ) {
	jQuery.fn[ name ] = function( until, selector ) {
		var matched = jQuery.map( this, fn, until );

		if ( name.slice( -5 ) !== "Until" ) {
			selector = until;
		}

		if ( selector && typeof selector === "string" ) {
			matched = jQuery.filter( selector, matched );
		}

		if ( this.length > 1 ) {

			// Remove duplicates
			if ( !guaranteedUnique[ name ] ) {
				jQuery.uniqueSort( matched );
			}

			// Reverse order for parents* and prev-derivatives
			if ( rparentsprev.test( name ) ) {
				matched.reverse();
			}
		}

		return this.pushStack( matched );
	};
} );
var rnothtmlwhite = ( /[^\x20\t\r\n\f]+/g );



// Convert String-formatted options into Object-formatted ones
function createOptions( options ) {
	var object = {};
	jQuery.each( options.match( rnothtmlwhite ) || [], function( _, flag ) {
		object[ flag ] = true;
	} );
	return object;
}

/*
 * Create a callback list using the following parameters:
 *
 *	options: an optional list of space-separated options that will change how
 *			the callback list behaves or a more traditional option object
 *
 * By default a callback list will act like an event callback list and can be
 * "fired" multiple times.
 *
 * Possible options:
 *
 *	once:			will ensure the callback list can only be fired once (like a Deferred)
 *
 *	memory:			will keep track of previous values and will call any callback added
 *					after the list has been fired right away with the latest "memorized"
 *					values (like a Deferred)
 *
 *	unique:			will ensure a callback can only be added once (no duplicate in the list)
 *
 *	stopOnFalse:	interrupt callings when a callback returns false
 *
 */
jQuery.Callbacks = function( options ) {

	// Convert options from String-formatted to Object-formatted if needed
	// (we check in cache first)
	options = typeof options === "string" ?
		createOptions( options ) :
		jQuery.extend( {}, options );

	var // Flag to know if list is currently firing
		firing,

		// Last fire value for non-forgettable lists
		memory,

		// Flag to know if list was already fired
		fired,

		// Flag to prevent firing
		locked,

		// Actual callback list
		list = [],

		// Queue of execution data for repeatable lists
		queue = [],

		// Index of currently firing callback (modified by add/remove as needed)
		firingIndex = -1,

		// Fire callbacks
		fire = function() {

			// Enforce single-firing
			locked = locked || options.once;

			// Execute callbacks for all pending executions,
			// respecting firingIndex overrides and runtime changes
			fired = firing = true;
			for ( ; queue.length; firingIndex = -1 ) {
				memory = queue.shift();
				while ( ++firingIndex < list.length ) {

					// Run callback and check for early termination
					if ( list[ firingIndex ].apply( memory[ 0 ], memory[ 1 ] ) === false &&
						options.stopOnFalse ) {

						// Jump to end and forget the data so .add doesn't re-fire
						firingIndex = list.length;
						memory = false;
					}
				}
			}

			// Forget the data if we're done with it
			if ( !options.memory ) {
				memory = false;
			}

			firing = false;

			// Clean up if we're done firing for good
			if ( locked ) {

				// Keep an empty list if we have data for future add calls
				if ( memory ) {
					list = [];

				// Otherwise, this object is spent
				} else {
					list = "";
				}
			}
		},

		// Actual Callbacks object
		self = {

			// Add a callback or a collection of callbacks to the list
			add: function() {
				if ( list ) {

					// If we have memory from a past run, we should fire after adding
					if ( memory && !firing ) {
						firingIndex = list.length - 1;
						queue.push( memory );
					}

					( function add( args ) {
						jQuery.each( args, function( _, arg ) {
							if ( isFunction( arg ) ) {
								if ( !options.unique || !self.has( arg ) ) {
									list.push( arg );
								}
							} else if ( arg && arg.length && toType( arg ) !== "string" ) {

								// Inspect recursively
								add( arg );
							}
						} );
					} )( arguments );

					if ( memory && !firing ) {
						fire();
					}
				}
				return this;
			},

			// Remove a callback from the list
			remove: function() {
				jQuery.each( arguments, function( _, arg ) {
					var index;
					while ( ( index = jQuery.inArray( arg, list, index ) ) > -1 ) {
						list.splice( index, 1 );

						// Handle firing indexes
						if ( index <= firingIndex ) {
							firingIndex--;
						}
					}
				} );
				return this;
			},

			// Check if a given callback is in the list.
			// If no argument is given, return whether or not list has callbacks attached.
			has: function( fn ) {
				return fn ?
					jQuery.inArray( fn, list ) > -1 :
					list.length > 0;
			},

			// Remove all callbacks from the list
			empty: function() {
				if ( list ) {
					list = [];
				}
				return this;
			},

			// Disable .fire and .add
			// Abort any current/pending executions
			// Clear all callbacks and values
			disable: function() {
				locked = queue = [];
				list = memory = "";
				return this;
			},
			disabled: function() {
				return !list;
			},

			// Disable .fire
			// Also disable .add unless we have memory (since it would have no effect)
			// Abort any pending executions
			lock: function() {
				locked = queue = [];
				if ( !memory && !firing ) {
					list = memory = "";
				}
				return this;
			},
			locked: function() {
				return !!locked;
			},

			// Call all callbacks with the given context and arguments
			fireWith: function( context, args ) {
				if ( !locked ) {
					args = args || [];
					args = [ context, args.slice ? args.slice() : args ];
					queue.push( args );
					if ( !firing ) {
						fire();
					}
				}
				return this;
			},

			// Call all the callbacks with the given arguments
			fire: function() {
				self.fireWith( this, arguments );
				return this;
			},

			// To know if the callbacks have already been called at least once
			fired: function() {
				return !!fired;
			}
		};

	return self;
};


function Identity( v ) {
	return v;
}
function Thrower( ex ) {
	throw ex;
}

function adoptValue( value, resolve, reject, noValue ) {
	var method;

	try {

		// Check for promise aspect first to privilege synchronous behavior
		if ( value && isFunction( ( method = value.promise ) ) ) {
			method.call( value ).done( resolve ).fail( reject );

		// Other thenables
		} else if ( value && isFunction( ( method = value.then ) ) ) {
			method.call( value, resolve, reject );

		// Other non-thenables
		} else {

			// Control `resolve` arguments by letting Array#slice cast boolean `noValue` to integer:
			// * false: [ value ].slice( 0 ) => resolve( value )
			// * true: [ value ].slice( 1 ) => resolve()
			resolve.apply( undefined, [ value ].slice( noValue ) );
		}

	// For Promises/A+, convert exceptions into rejections
	// Since jQuery.when doesn't unwrap thenables, we can skip the extra checks appearing in
	// Deferred#then to conditionally suppress rejection.
	} catch ( value ) {

		// Support: Android 4.0 only
		// Strict mode functions invoked without .call/.apply get global-object context
		reject.apply( undefined, [ value ] );
	}
}

jQuery.extend( {

	Deferred: function( func ) {
		var tuples = [

				// action, add listener, callbacks,
				// ... .then handlers, argument index, [final state]
				[ "notify", "progress", jQuery.Callbacks( "memory" ),
					jQuery.Callbacks( "memory" ), 2 ],
				[ "resolve", "done", jQuery.Callbacks( "once memory" ),
					jQuery.Callbacks( "once memory" ), 0, "resolved" ],
				[ "reject", "fail", jQuery.Callbacks( "once memory" ),
					jQuery.Callbacks( "once memory" ), 1, "rejected" ]
			],
			state = "pending",
			promise = {
				state: function() {
					return state;
				},
				always: function() {
					deferred.done( arguments ).fail( arguments );
					return this;
				},
				"catch": function( fn ) {
					return promise.then( null, fn );
				},

				// Keep pipe for back-compat
				pipe: function( /* fnDone, fnFail, fnProgress */ ) {
					var fns = arguments;

					return jQuery.Deferred( function( newDefer ) {
						jQuery.each( tuples, function( _i, tuple ) {

							// Map tuples (progress, done, fail) to arguments (done, fail, progress)
							var fn = isFunction( fns[ tuple[ 4 ] ] ) && fns[ tuple[ 4 ] ];

							// deferred.progress(function() { bind to newDefer or newDefer.notify })
							// deferred.done(function() { bind to newDefer or newDefer.resolve })
							// deferred.fail(function() { bind to newDefer or newDefer.reject })
							deferred[ tuple[ 1 ] ]( function() {
								var returned = fn && fn.apply( this, arguments );
								if ( returned && isFunction( returned.promise ) ) {
									returned.promise()
										.progress( newDefer.notify )
										.done( newDefer.resolve )
										.fail( newDefer.reject );
								} else {
									newDefer[ tuple[ 0 ] + "With" ](
										this,
										fn ? [ returned ] : arguments
									);
								}
							} );
						} );
						fns = null;
					} ).promise();
				},
				then: function( onFulfilled, onRejected, onProgress ) {
					var maxDepth = 0;
					function resolve( depth, deferred, handler, special ) {
						return function() {
							var that = this,
								args = arguments,
								mightThrow = function() {
									var returned, then;

									// Support: Promises/A+ section 2.3.3.3.3
									// https://promisesaplus.com/#point-59
									// Ignore double-resolution attempts
									if ( depth < maxDepth ) {
										return;
									}

									returned = handler.apply( that, args );

									// Support: Promises/A+ section 2.3.1
									// https://promisesaplus.com/#point-48
									if ( returned === deferred.promise() ) {
										throw new TypeError( "Thenable self-resolution" );
									}

									// Support: Promises/A+ sections 2.3.3.1, 3.5
									// https://promisesaplus.com/#point-54
									// https://promisesaplus.com/#point-75
									// Retrieve `then` only once
									then = returned &&

										// Support: Promises/A+ section 2.3.4
										// https://promisesaplus.com/#point-64
										// Only check objects and functions for thenability
										( typeof returned === "object" ||
											typeof returned === "function" ) &&
										returned.then;

									// Handle a returned thenable
									if ( isFunction( then ) ) {

										// Special processors (notify) just wait for resolution
										if ( special ) {
											then.call(
												returned,
												resolve( maxDepth, deferred, Identity, special ),
												resolve( maxDepth, deferred, Thrower, special )
											);

										// Normal processors (resolve) also hook into progress
										} else {

											// ...and disregard older resolution values
											maxDepth++;

											then.call(
												returned,
												resolve( maxDepth, deferred, Identity, special ),
												resolve( maxDepth, deferred, Thrower, special ),
												resolve( maxDepth, deferred, Identity,
													deferred.notifyWith )
											);
										}

									// Handle all other returned values
									} else {

										// Only substitute handlers pass on context
										// and multiple values (non-spec behavior)
										if ( handler !== Identity ) {
											that = undefined;
											args = [ returned ];
										}

										// Process the value(s)
										// Default process is resolve
										( special || deferred.resolveWith )( that, args );
									}
								},

								// Only normal processors (resolve) catch and reject exceptions
								process = special ?
									mightThrow :
									function() {
										try {
											mightThrow();
										} catch ( e ) {

											if ( jQuery.Deferred.exceptionHook ) {
												jQuery.Deferred.exceptionHook( e,
													process.stackTrace );
											}

											// Support: Promises/A+ section 2.3.3.3.4.1
											// https://promisesaplus.com/#point-61
											// Ignore post-resolution exceptions
											if ( depth + 1 >= maxDepth ) {

												// Only substitute handlers pass on context
												// and multiple values (non-spec behavior)
												if ( handler !== Thrower ) {
													that = undefined;
													args = [ e ];
												}

												deferred.rejectWith( that, args );
											}
										}
									};

							// Support: Promises/A+ section 2.3.3.3.1
							// https://promisesaplus.com/#point-57
							// Re-resolve promises immediately to dodge false rejection from
							// subsequent errors
							if ( depth ) {
								process();
							} else {

								// Call an optional hook to record the stack, in case of exception
								// since it's otherwise lost when execution goes async
								if ( jQuery.Deferred.getStackHook ) {
									process.stackTrace = jQuery.Deferred.getStackHook();
								}
								window.setTimeout( process );
							}
						};
					}

					return jQuery.Deferred( function( newDefer ) {

						// progress_handlers.add( ... )
						tuples[ 0 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onProgress ) ?
									onProgress :
									Identity,
								newDefer.notifyWith
							)
						);

						// fulfilled_handlers.add( ... )
						tuples[ 1 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onFulfilled ) ?
									onFulfilled :
									Identity
							)
						);

						// rejected_handlers.add( ... )
						tuples[ 2 ][ 3 ].add(
							resolve(
								0,
								newDefer,
								isFunction( onRejected ) ?
									onRejected :
									Thrower
							)
						);
					} ).promise();
				},

				// Get a promise for this deferred
				// If obj is provided, the promise aspect is added to the object
				promise: function( obj ) {
					return obj != null ? jQuery.extend( obj, promise ) : promise;
				}
			},
			deferred = {};

		// Add list-specific methods
		jQuery.each( tuples, function( i, tuple ) {
			var list = tuple[ 2 ],
				stateString = tuple[ 5 ];

			// promise.progress = list.add
			// promise.done = list.add
			// promise.fail = list.add
			promise[ tuple[ 1 ] ] = list.add;

			// Handle state
			if ( stateString ) {
				list.add(
					function() {

						// state = "resolved" (i.e., fulfilled)
						// state = "rejected"
						state = stateString;
					},

					// rejected_callbacks.disable
					// fulfilled_callbacks.disable
					tuples[ 3 - i ][ 2 ].disable,

					// rejected_handlers.disable
					// fulfilled_handlers.disable
					tuples[ 3 - i ][ 3 ].disable,

					// progress_callbacks.lock
					tuples[ 0 ][ 2 ].lock,

					// progress_handlers.lock
					tuples[ 0 ][ 3 ].lock
				);
			}

			// progress_handlers.fire
			// fulfilled_handlers.fire
			// rejected_handlers.fire
			list.add( tuple[ 3 ].fire );

			// deferred.notify = function() { deferred.notifyWith(...) }
			// deferred.resolve = function() { deferred.resolveWith(...) }
			// deferred.reject = function() { deferred.rejectWith(...) }
			deferred[ tuple[ 0 ] ] = function() {
				deferred[ tuple[ 0 ] + "With" ]( this === deferred ? undefined : this, arguments );
				return this;
			};

			// deferred.notifyWith = list.fireWith
			// deferred.resolveWith = list.fireWith
			// deferred.rejectWith = list.fireWith
			deferred[ tuple[ 0 ] + "With" ] = list.fireWith;
		} );

		// Make the deferred a promise
		promise.promise( deferred );

		// Call given func if any
		if ( func ) {
			func.call( deferred, deferred );
		}

		// All done!
		return deferred;
	},

	// Deferred helper
	when: function( singleValue ) {
		var

			// count of uncompleted subordinates
			remaining = arguments.length,

			// count of unprocessed arguments
			i = remaining,

			// subordinate fulfillment data
			resolveContexts = Array( i ),
			resolveValues = slice.call( arguments ),

			// the master Deferred
			master = jQuery.Deferred(),

			// subordinate callback factory
			updateFunc = function( i ) {
				return function( value ) {
					resolveContexts[ i ] = this;
					resolveValues[ i ] = arguments.length > 1 ? slice.call( arguments ) : value;
					if ( !( --remaining ) ) {
						master.resolveWith( resolveContexts, resolveValues );
					}
				};
			};

		// Single- and empty arguments are adopted like Promise.resolve
		if ( remaining <= 1 ) {
			adoptValue( singleValue, master.done( updateFunc( i ) ).resolve, master.reject,
				!remaining );

			// Use .then() to unwrap secondary thenables (cf. gh-3000)
			if ( master.state() === "pending" ||
				isFunction( resolveValues[ i ] && resolveValues[ i ].then ) ) {

				return master.then();
			}
		}

		// Multiple arguments are aggregated like Promise.all array elements
		while ( i-- ) {
			adoptValue( resolveValues[ i ], updateFunc( i ), master.reject );
		}

		return master.promise();
	}
} );


// These usually indicate a programmer mistake during development,
// warn about them ASAP rather than swallowing them by default.
var rerrorNames = /^(Eval|Internal|Range|Reference|Syntax|Type|URI)Error$/;

jQuery.Deferred.exceptionHook = function( error, stack ) {

	// Support: IE 8 - 9 only
	// Console exists when dev tools are open, which can happen at any time
	if ( window.console && window.console.warn && error && rerrorNames.test( error.name ) ) {
		window.console.warn( "jQuery.Deferred exception: " + error.message, error.stack, stack );
	}
};




jQuery.readyException = function( error ) {
	window.setTimeout( function() {
		throw error;
	} );
};




// The deferred used on DOM ready
var readyList = jQuery.Deferred();

jQuery.fn.ready = function( fn ) {

	readyList
		.then( fn )

		// Wrap jQuery.readyException in a function so that the lookup
		// happens at the time of error handling instead of callback
		// registration.
		.catch( function( error ) {
			jQuery.readyException( error );
		} );

	return this;
};

jQuery.extend( {

	// Is the DOM ready to be used? Set to true once it occurs.
	isReady: false,

	// A counter to track how many items to wait for before
	// the ready event fires. See #6781
	readyWait: 1,

	// Handle when the DOM is ready
	ready: function( wait ) {

		// Abort if there are pending holds or we're already ready
		if ( wait === true ? --jQuery.readyWait : jQuery.isReady ) {
			return;
		}

		// Remember that the DOM is ready
		jQuery.isReady = true;

		// If a normal DOM Ready event fired, decrement, and wait if need be
		if ( wait !== true && --jQuery.readyWait > 0 ) {
			return;
		}

		// If there are functions bound, to execute
		readyList.resolveWith( document, [ jQuery ] );
	}
} );

jQuery.ready.then = readyList.then;

// The ready event handler and self cleanup method
function completed() {
	document.removeEventListener( "DOMContentLoaded", completed );
	window.removeEventListener( "load", completed );
	jQuery.ready();
}

// Catch cases where $(document).ready() is called
// after the browser event has already occurred.
// Support: IE <=9 - 10 only
// Older IE sometimes signals "interactive" too soon
if ( document.readyState === "complete" ||
	( document.readyState !== "loading" && !document.documentElement.doScroll ) ) {

	// Handle it asynchronously to allow scripts the opportunity to delay ready
	window.setTimeout( jQuery.ready );

} else {

	// Use the handy event callback
	document.addEventListener( "DOMContentLoaded", completed );

	// A fallback to window.onload, that will always work
	window.addEventListener( "load", completed );
}




// Multifunctional method to get and set values of a collection
// The value/s can optionally be executed if it's a function
var access = function( elems, fn, key, value, chainable, emptyGet, raw ) {
	var i = 0,
		len = elems.length,
		bulk = key == null;

	// Sets many values
	if ( toType( key ) === "object" ) {
		chainable = true;
		for ( i in key ) {
			access( elems, fn, i, key[ i ], true, emptyGet, raw );
		}

	// Sets one value
	} else if ( value !== undefined ) {
		chainable = true;

		if ( !isFunction( value ) ) {
			raw = true;
		}

		if ( bulk ) {

			// Bulk operations run against the entire set
			if ( raw ) {
				fn.call( elems, value );
				fn = null;

			// ...except when executing function values
			} else {
				bulk = fn;
				fn = function( elem, _key, value ) {
					return bulk.call( jQuery( elem ), value );
				};
			}
		}

		if ( fn ) {
			for ( ; i < len; i++ ) {
				fn(
					elems[ i ], key, raw ?
					value :
					value.call( elems[ i ], i, fn( elems[ i ], key ) )
				);
			}
		}
	}

	if ( chainable ) {
		return elems;
	}

	// Gets
	if ( bulk ) {
		return fn.call( elems );
	}

	return len ? fn( elems[ 0 ], key ) : emptyGet;
};


// Matches dashed string for camelizing
var rmsPrefix = /^-ms-/,
	rdashAlpha = /-([a-z])/g;

// Used by camelCase as callback to replace()
function fcamelCase( _all, letter ) {
	return letter.toUpperCase();
}

// Convert dashed to camelCase; used by the css and data modules
// Support: IE <=9 - 11, Edge 12 - 15
// Microsoft forgot to hump their vendor prefix (#9572)
function camelCase( string ) {
	return string.replace( rmsPrefix, "ms-" ).replace( rdashAlpha, fcamelCase );
}
var acceptData = function( owner ) {

	// Accepts only:
	//  - Node
	//    - Node.ELEMENT_NODE
	//    - Node.DOCUMENT_NODE
	//  - Object
	//    - Any
	return owner.nodeType === 1 || owner.nodeType === 9 || !( +owner.nodeType );
};




function Data() {
	this.expando = jQuery.expando + Data.uid++;
}

Data.uid = 1;

Data.prototype = {

	cache: function( owner ) {

		// Check if the owner object already has a cache
		var value = owner[ this.expando ];

		// If not, create one
		if ( !value ) {
			value = {};

			// We can accept data for non-element nodes in modern browsers,
			// but we should not, see #8335.
			// Always return an empty object.
			if ( acceptData( owner ) ) {

				// If it is a node unlikely to be stringify-ed or looped over
				// use plain assignment
				if ( owner.nodeType ) {
					owner[ this.expando ] = value;

				// Otherwise secure it in a non-enumerable property
				// configurable must be true to allow the property to be
				// deleted when data is removed
				} else {
					Object.defineProperty( owner, this.expando, {
						value: value,
						configurable: true
					} );
				}
			}
		}

		return value;
	},
	set: function( owner, data, value ) {
		var prop,
			cache = this.cache( owner );

		// Handle: [ owner, key, value ] args
		// Always use camelCase key (gh-2257)
		if ( typeof data === "string" ) {
			cache[ camelCase( data ) ] = value;

		// Handle: [ owner, { properties } ] args
		} else {

			// Copy the properties one-by-one to the cache object
			for ( prop in data ) {
				cache[ camelCase( prop ) ] = data[ prop ];
			}
		}
		return cache;
	},
	get: function( owner, key ) {
		return key === undefined ?
			this.cache( owner ) :

			// Always use camelCase key (gh-2257)
			owner[ this.expando ] && owner[ this.expando ][ camelCase( key ) ];
	},
	access: function( owner, key, value ) {

		// In cases where either:
		//
		//   1. No key was specified
		//   2. A string key was specified, but no value provided
		//
		// Take the "read" path and allow the get method to determine
		// which value to return, respectively either:
		//
		//   1. The entire cache object
		//   2. The data stored at the key
		//
		if ( key === undefined ||
				( ( key && typeof key === "string" ) && value === undefined ) ) {

			return this.get( owner, key );
		}

		// When the key is not a string, or both a key and value
		// are specified, set or extend (existing objects) with either:
		//
		//   1. An object of properties
		//   2. A key and value
		//
		this.set( owner, key, value );

		// Since the "set" path can have two possible entry points
		// return the expected data based on which path was taken[*]
		return value !== undefined ? value : key;
	},
	remove: function( owner, key ) {
		var i,
			cache = owner[ this.expando ];

		if ( cache === undefined ) {
			return;
		}

		if ( key !== undefined ) {

			// Support array or space separated string of keys
			if ( Array.isArray( key ) ) {

				// If key is an array of keys...
				// We always set camelCase keys, so remove that.
				key = key.map( camelCase );
			} else {
				key = camelCase( key );

				// If a key with the spaces exists, use it.
				// Otherwise, create an array by matching non-whitespace
				key = key in cache ?
					[ key ] :
					( key.match( rnothtmlwhite ) || [] );
			}

			i = key.length;

			while ( i-- ) {
				delete cache[ key[ i ] ];
			}
		}

		// Remove the expando if there's no more data
		if ( key === undefined || jQuery.isEmptyObject( cache ) ) {

			// Support: Chrome <=35 - 45
			// Webkit & Blink performance suffers when deleting properties
			// from DOM nodes, so set to undefined instead
			// https://bugs.chromium.org/p/chromium/issues/detail?id=378607 (bug restricted)
			if ( owner.nodeType ) {
				owner[ this.expando ] = undefined;
			} else {
				delete owner[ this.expando ];
			}
		}
	},
	hasData: function( owner ) {
		var cache = owner[ this.expando ];
		return cache !== undefined && !jQuery.isEmptyObject( cache );
	}
};
var dataPriv = new Data();

var dataUser = new Data();



//	Implementation Summary
//
//	1. Enforce API surface and semantic compatibility with 1.9.x branch
//	2. Improve the module's maintainability by reducing the storage
//		paths to a single mechanism.
//	3. Use the same single mechanism to support "private" and "user" data.
//	4. _Never_ expose "private" data to user code (TODO: Drop _data, _removeData)
//	5. Avoid exposing implementation details on user objects (eg. expando properties)
//	6. Provide a clear path for implementation upgrade to WeakMap in 2014

var rbrace = /^(?:\{[\w\W]*\}|\[[\w\W]*\])$/,
	rmultiDash = /[A-Z]/g;

function getData( data ) {
	if ( data === "true" ) {
		return true;
	}

	if ( data === "false" ) {
		return false;
	}

	if ( data === "null" ) {
		return null;
	}

	// Only convert to a number if it doesn't change the string
	if ( data === +data + "" ) {
		return +data;
	}

	if ( rbrace.test( data ) ) {
		return JSON.parse( data );
	}

	return data;
}

function dataAttr( elem, key, data ) {
	var name;

	// If nothing was found internally, try to fetch any
	// data from the HTML5 data-* attribute
	if ( data === undefined && elem.nodeType === 1 ) {
		name = "data-" + key.replace( rmultiDash, "-$&" ).toLowerCase();
		data = elem.getAttribute( name );

		if ( typeof data === "string" ) {
			try {
				data = getData( data );
			} catch ( e ) {}

			// Make sure we set the data so it isn't changed later
			dataUser.set( elem, key, data );
		} else {
			data = undefined;
		}
	}
	return data;
}

jQuery.extend( {
	hasData: function( elem ) {
		return dataUser.hasData( elem ) || dataPriv.hasData( elem );
	},

	data: function( elem, name, data ) {
		return dataUser.access( elem, name, data );
	},

	removeData: function( elem, name ) {
		dataUser.remove( elem, name );
	},

	// TODO: Now that all calls to _data and _removeData have been replaced
	// with direct calls to dataPriv methods, these can be deprecated.
	_data: function( elem, name, data ) {
		return dataPriv.access( elem, name, data );
	},

	_removeData: function( elem, name ) {
		dataPriv.remove( elem, name );
	}
} );

jQuery.fn.extend( {
	data: function( key, value ) {
		var i, name, data,
			elem = this[ 0 ],
			attrs = elem && elem.attributes;

		// Gets all values
		if ( key === undefined ) {
			if ( this.length ) {
				data = dataUser.get( elem );

				if ( elem.nodeType === 1 && !dataPriv.get( elem, "hasDataAttrs" ) ) {
					i = attrs.length;
					while ( i-- ) {

						// Support: IE 11 only
						// The attrs elements can be null (#14894)
						if ( attrs[ i ] ) {
							name = attrs[ i ].name;
							if ( name.indexOf( "data-" ) === 0 ) {
								name = camelCase( name.slice( 5 ) );
								dataAttr( elem, name, data[ name ] );
							}
						}
					}
					dataPriv.set( elem, "hasDataAttrs", true );
				}
			}

			return data;
		}

		// Sets multiple values
		if ( typeof key === "object" ) {
			return this.each( function() {
				dataUser.set( this, key );
			} );
		}

		return access( this, function( value ) {
			var data;

			// The calling jQuery object (element matches) is not empty
			// (and therefore has an element appears at this[ 0 ]) and the
			// `value` parameter was not undefined. An empty jQuery object
			// will result in `undefined` for elem = this[ 0 ] which will
			// throw an exception if an attempt to read a data cache is made.
			if ( elem && value === undefined ) {

				// Attempt to get data from the cache
				// The key will always be camelCased in Data
				data = dataUser.get( elem, key );
				if ( data !== undefined ) {
					return data;
				}

				// Attempt to "discover" the data in
				// HTML5 custom data-* attrs
				data = dataAttr( elem, key );
				if ( data !== undefined ) {
					return data;
				}

				// We tried really hard, but the data doesn't exist.
				return;
			}

			// Set the data...
			this.each( function() {

				// We always store the camelCased key
				dataUser.set( this, key, value );
			} );
		}, null, value, arguments.length > 1, null, true );
	},

	removeData: function( key ) {
		return this.each( function() {
			dataUser.remove( this, key );
		} );
	}
} );


jQuery.extend( {
	queue: function( elem, type, data ) {
		var queue;

		if ( elem ) {
			type = ( type || "fx" ) + "queue";
			queue = dataPriv.get( elem, type );

			// Speed up dequeue by getting out quickly if this is just a lookup
			if ( data ) {
				if ( !queue || Array.isArray( data ) ) {
					queue = dataPriv.access( elem, type, jQuery.makeArray( data ) );
				} else {
					queue.push( data );
				}
			}
			return queue || [];
		}
	},

	dequeue: function( elem, type ) {
		type = type || "fx";

		var queue = jQuery.queue( elem, type ),
			startLength = queue.length,
			fn = queue.shift(),
			hooks = jQuery._queueHooks( elem, type ),
			next = function() {
				jQuery.dequeue( elem, type );
			};

		// If the fx queue is dequeued, always remove the progress sentinel
		if ( fn === "inprogress" ) {
			fn = queue.shift();
			startLength--;
		}

		if ( fn ) {

			// Add a progress sentinel to prevent the fx queue from being
			// automatically dequeued
			if ( type === "fx" ) {
				queue.unshift( "inprogress" );
			}

			// Clear up the last queue stop function
			delete hooks.stop;
			fn.call( elem, next, hooks );
		}

		if ( !startLength && hooks ) {
			hooks.empty.fire();
		}
	},

	// Not public - generate a queueHooks object, or return the current one
	_queueHooks: function( elem, type ) {
		var key = type + "queueHooks";
		return dataPriv.get( elem, key ) || dataPriv.access( elem, key, {
			empty: jQuery.Callbacks( "once memory" ).add( function() {
				dataPriv.remove( elem, [ type + "queue", key ] );
			} )
		} );
	}
} );

jQuery.fn.extend( {
	queue: function( type, data ) {
		var setter = 2;

		if ( typeof type !== "string" ) {
			data = type;
			type = "fx";
			setter--;
		}

		if ( arguments.length < setter ) {
			return jQuery.queue( this[ 0 ], type );
		}

		return data === undefined ?
			this :
			this.each( function() {
				var queue = jQuery.queue( this, type, data );

				// Ensure a hooks for this queue
				jQuery._queueHooks( this, type );

				if ( type === "fx" && queue[ 0 ] !== "inprogress" ) {
					jQuery.dequeue( this, type );
				}
			} );
	},
	dequeue: function( type ) {
		return this.each( function() {
			jQuery.dequeue( this, type );
		} );
	},
	clearQueue: function( type ) {
		return this.queue( type || "fx", [] );
	},

	// Get a promise resolved when queues of a certain type
	// are emptied (fx is the type by default)
	promise: function( type, obj ) {
		var tmp,
			count = 1,
			defer = jQuery.Deferred(),
			elements = this,
			i = this.length,
			resolve = function() {
				if ( !( --count ) ) {
					defer.resolveWith( elements, [ elements ] );
				}
			};

		if ( typeof type !== "string" ) {
			obj = type;
			type = undefined;
		}
		type = type || "fx";

		while ( i-- ) {
			tmp = dataPriv.get( elements[ i ], type + "queueHooks" );
			if ( tmp && tmp.empty ) {
				count++;
				tmp.empty.add( resolve );
			}
		}
		resolve();
		return defer.promise( obj );
	}
} );
var pnum = ( /[+-]?(?:\d*\.|)\d+(?:[eE][+-]?\d+|)/ ).source;

var rcssNum = new RegExp( "^(?:([+-])=|)(" + pnum + ")([a-z%]*)$", "i" );


var cssExpand = [ "Top", "Right", "Bottom", "Left" ];

var documentElement = document.documentElement;



	var isAttached = function( elem ) {
			return jQuery.contains( elem.ownerDocument, elem );
		},
		composed = { composed: true };

	// Support: IE 9 - 11+, Edge 12 - 18+, iOS 10.0 - 10.2 only
	// Check attachment across shadow DOM boundaries when possible (gh-3504)
	// Support: iOS 10.0-10.2 only
	// Early iOS 10 versions support `attachShadow` but not `getRootNode`,
	// leading to errors. We need to check for `getRootNode`.
	if ( documentElement.getRootNode ) {
		isAttached = function( elem ) {
			return jQuery.contains( elem.ownerDocument, elem ) ||
				elem.getRootNode( composed ) === elem.ownerDocument;
		};
	}
var isHiddenWithinTree = function( elem, el ) {

		// isHiddenWithinTree might be called from jQuery#filter function;
		// in that case, element will be second argument
		elem = el || elem;

		// Inline style trumps all
		return elem.style.display === "none" ||
			elem.style.display === "" &&

			// Otherwise, check computed style
			// Support: Firefox <=43 - 45
			// Disconnected elements can have computed display: none, so first confirm that elem is
			// in the document.
			isAttached( elem ) &&

			jQuery.css( elem, "display" ) === "none";
	};



function adjustCSS( elem, prop, valueParts, tween ) {
	var adjusted, scale,
		maxIterations = 20,
		currentValue = tween ?
			function() {
				return tween.cur();
			} :
			function() {
				return jQuery.css( elem, prop, "" );
			},
		initial = currentValue(),
		unit = valueParts && valueParts[ 3 ] || ( jQuery.cssNumber[ prop ] ? "" : "px" ),

		// Starting value computation is required for potential unit mismatches
		initialInUnit = elem.nodeType &&
			( jQuery.cssNumber[ prop ] || unit !== "px" && +initial ) &&
			rcssNum.exec( jQuery.css( elem, prop ) );

	if ( initialInUnit && initialInUnit[ 3 ] !== unit ) {

		// Support: Firefox <=54
		// Halve the iteration target value to prevent interference from CSS upper bounds (gh-2144)
		initial = initial / 2;

		// Trust units reported by jQuery.css
		unit = unit || initialInUnit[ 3 ];

		// Iteratively approximate from a nonzero starting point
		initialInUnit = +initial || 1;

		while ( maxIterations-- ) {

			// Evaluate and update our best guess (doubling guesses that zero out).
			// Finish if the scale equals or crosses 1 (making the old*new product non-positive).
			jQuery.style( elem, prop, initialInUnit + unit );
			if ( ( 1 - scale ) * ( 1 - ( scale = currentValue() / initial || 0.5 ) ) <= 0 ) {
				maxIterations = 0;
			}
			initialInUnit = initialInUnit / scale;

		}

		initialInUnit = initialInUnit * 2;
		jQuery.style( elem, prop, initialInUnit + unit );

		// Make sure we update the tween properties later on
		valueParts = valueParts || [];
	}

	if ( valueParts ) {
		initialInUnit = +initialInUnit || +initial || 0;

		// Apply relative offset (+=/-=) if specified
		adjusted = valueParts[ 1 ] ?
			initialInUnit + ( valueParts[ 1 ] + 1 ) * valueParts[ 2 ] :
			+valueParts[ 2 ];
		if ( tween ) {
			tween.unit = unit;
			tween.start = initialInUnit;
			tween.end = adjusted;
		}
	}
	return adjusted;
}


var defaultDisplayMap = {};

function getDefaultDisplay( elem ) {
	var temp,
		doc = elem.ownerDocument,
		nodeName = elem.nodeName,
		display = defaultDisplayMap[ nodeName ];

	if ( display ) {
		return display;
	}

	temp = doc.body.appendChild( doc.createElement( nodeName ) );
	display = jQuery.css( temp, "display" );

	temp.parentNode.removeChild( temp );

	if ( display === "none" ) {
		display = "block";
	}
	defaultDisplayMap[ nodeName ] = display;

	return display;
}

function showHide( elements, show ) {
	var display, elem,
		values = [],
		index = 0,
		length = elements.length;

	// Determine new display value for elements that need to change
	for ( ; index < length; index++ ) {
		elem = elements[ index ];
		if ( !elem.style ) {
			continue;
		}

		display = elem.style.display;
		if ( show ) {

			// Since we force visibility upon cascade-hidden elements, an immediate (and slow)
			// check is required in this first loop unless we have a nonempty display value (either
			// inline or about-to-be-restored)
			if ( display === "none" ) {
				values[ index ] = dataPriv.get( elem, "display" ) || null;
				if ( !values[ index ] ) {
					elem.style.display = "";
				}
			}
			if ( elem.style.display === "" && isHiddenWithinTree( elem ) ) {
				values[ index ] = getDefaultDisplay( elem );
			}
		} else {
			if ( display !== "none" ) {
				values[ index ] = "none";

				// Remember what we're overwriting
				dataPriv.set( elem, "display", display );
			}
		}
	}

	// Set the display of the elements in a second loop to avoid constant reflow
	for ( index = 0; index < length; index++ ) {
		if ( values[ index ] != null ) {
			elements[ index ].style.display = values[ index ];
		}
	}

	return elements;
}

jQuery.fn.extend( {
	show: function() {
		return showHide( this, true );
	},
	hide: function() {
		return showHide( this );
	},
	toggle: function( state ) {
		if ( typeof state === "boolean" ) {
			return state ? this.show() : this.hide();
		}

		return this.each( function() {
			if ( isHiddenWithinTree( this ) ) {
				jQuery( this ).show();
			} else {
				jQuery( this ).hide();
			}
		} );
	}
} );
var rcheckableType = ( /^(?:checkbox|radio)$/i );

var rtagName = ( /<([a-z][^\/\0>\x20\t\r\n\f]*)/i );

var rscriptType = ( /^$|^module$|\/(?:java|ecma)script/i );



( function() {
	var fragment = document.createDocumentFragment(),
		div = fragment.appendChild( document.createElement( "div" ) ),
		input = document.createElement( "input" );

	// Support: Android 4.0 - 4.3 only
	// Check state lost if the name is set (#11217)
	// Support: Windows Web Apps (WWA)
	// `name` and `type` must use .setAttribute for WWA (#14901)
	input.setAttribute( "type", "radio" );
	input.setAttribute( "checked", "checked" );
	input.setAttribute( "name", "t" );

	div.appendChild( input );

	// Support: Android <=4.1 only
	// Older WebKit doesn't clone checked state correctly in fragments
	support.checkClone = div.cloneNode( true ).cloneNode( true ).lastChild.checked;

	// Support: IE <=11 only
	// Make sure textarea (and checkbox) defaultValue is properly cloned
	div.innerHTML = "<textarea>x</textarea>";
	support.noCloneChecked = !!div.cloneNode( true ).lastChild.defaultValue;

	// Support: IE <=9 only
	// IE <=9 replaces <option> tags with their contents when inserted outside of
	// the select element.
	div.innerHTML = "<option></option>";
	support.option = !!div.lastChild;
} )();


// We have to close these tags to support XHTML (#13200)
var wrapMap = {

	// XHTML parsers do not magically insert elements in the
	// same way that tag soup parsers do. So we cannot shorten
	// this by omitting <tbody> or other required elements.
	thead: [ 1, "<table>", "</table>" ],
	col: [ 2, "<table><colgroup>", "</colgroup></table>" ],
	tr: [ 2, "<table><tbody>", "</tbody></table>" ],
	td: [ 3, "<table><tbody><tr>", "</tr></tbody></table>" ],

	_default: [ 0, "", "" ]
};

wrapMap.tbody = wrapMap.tfoot = wrapMap.colgroup = wrapMap.caption = wrapMap.thead;
wrapMap.th = wrapMap.td;

// Support: IE <=9 only
if ( !support.option ) {
	wrapMap.optgroup = wrapMap.option = [ 1, "<select multiple='multiple'>", "</select>" ];
}


function getAll( context, tag ) {

	// Support: IE <=9 - 11 only
	// Use typeof to avoid zero-argument method invocation on host objects (#15151)
	var ret;

	if ( typeof context.getElementsByTagName !== "undefined" ) {
		ret = context.getElementsByTagName( tag || "*" );

	} else if ( typeof context.querySelectorAll !== "undefined" ) {
		ret = context.querySelectorAll( tag || "*" );

	} else {
		ret = [];
	}

	if ( tag === undefined || tag && nodeName( context, tag ) ) {
		return jQuery.merge( [ context ], ret );
	}

	return ret;
}


// Mark scripts as having already been evaluated
function setGlobalEval( elems, refElements ) {
	var i = 0,
		l = elems.length;

	for ( ; i < l; i++ ) {
		dataPriv.set(
			elems[ i ],
			"globalEval",
			!refElements || dataPriv.get( refElements[ i ], "globalEval" )
		);
	}
}


var rhtml = /<|&#?\w+;/;

function buildFragment( elems, context, scripts, selection, ignored ) {
	var elem, tmp, tag, wrap, attached, j,
		fragment = context.createDocumentFragment(),
		nodes = [],
		i = 0,
		l = elems.length;

	for ( ; i < l; i++ ) {
		elem = elems[ i ];

		if ( elem || elem === 0 ) {

			// Add nodes directly
			if ( toType( elem ) === "object" ) {

				// Support: Android <=4.0 only, PhantomJS 1 only
				// push.apply(_, arraylike) throws on ancient WebKit
				jQuery.merge( nodes, elem.nodeType ? [ elem ] : elem );

			// Convert non-html into a text node
			} else if ( !rhtml.test( elem ) ) {
				nodes.push( context.createTextNode( elem ) );

			// Convert html into DOM nodes
			} else {
				tmp = tmp || fragment.appendChild( context.createElement( "div" ) );

				// Deserialize a standard representation
				tag = ( rtagName.exec( elem ) || [ "", "" ] )[ 1 ].toLowerCase();
				wrap = wrapMap[ tag ] || wrapMap._default;
				tmp.innerHTML = wrap[ 1 ] + jQuery.htmlPrefilter( elem ) + wrap[ 2 ];

				// Descend through wrappers to the right content
				j = wrap[ 0 ];
				while ( j-- ) {
					tmp = tmp.lastChild;
				}

				// Support: Android <=4.0 only, PhantomJS 1 only
				// push.apply(_, arraylike) throws on ancient WebKit
				jQuery.merge( nodes, tmp.childNodes );

				// Remember the top-level container
				tmp = fragment.firstChild;

				// Ensure the created nodes are orphaned (#12392)
				tmp.textContent = "";
			}
		}
	}

	// Remove wrapper from fragment
	fragment.textContent = "";

	i = 0;
	while ( ( elem = nodes[ i++ ] ) ) {

		// Skip elements already in the context collection (trac-4087)
		if ( selection && jQuery.inArray( elem, selection ) > -1 ) {
			if ( ignored ) {
				ignored.push( elem );
			}
			continue;
		}

		attached = isAttached( elem );

		// Append to fragment
		tmp = getAll( fragment.appendChild( elem ), "script" );

		// Preserve script evaluation history
		if ( attached ) {
			setGlobalEval( tmp );
		}

		// Capture executables
		if ( scripts ) {
			j = 0;
			while ( ( elem = tmp[ j++ ] ) ) {
				if ( rscriptType.test( elem.type || "" ) ) {
					scripts.push( elem );
				}
			}
		}
	}

	return fragment;
}


var
	rkeyEvent = /^key/,
	rmouseEvent = /^(?:mouse|pointer|contextmenu|drag|drop)|click/,
	rtypenamespace = /^([^.]*)(?:\.(.+)|)/;

function returnTrue() {
	return true;
}

function returnFalse() {
	return false;
}

// Support: IE <=9 - 11+
// focus() and blur() are asynchronous, except when they are no-op.
// So expect focus to be synchronous when the element is already active,
// and blur to be synchronous when the element is not already active.
// (focus and blur are always synchronous in other supported browsers,
// this just defines when we can count on it).
function expectSync( elem, type ) {
	return ( elem === safeActiveElement() ) === ( type === "focus" );
}

// Support: IE <=9 only
// Accessing document.activeElement can throw unexpectedly
// https://bugs.jquery.com/ticket/13393
function safeActiveElement() {
	try {
		return document.activeElement;
	} catch ( err ) { }
}

function on( elem, types, selector, data, fn, one ) {
	var origFn, type;

	// Types can be a map of types/handlers
	if ( typeof types === "object" ) {

		// ( types-Object, selector, data )
		if ( typeof selector !== "string" ) {

			// ( types-Object, data )
			data = data || selector;
			selector = undefined;
		}
		for ( type in types ) {
			on( elem, type, selector, data, types[ type ], one );
		}
		return elem;
	}

	if ( data == null && fn == null ) {

		// ( types, fn )
		fn = selector;
		data = selector = undefined;
	} else if ( fn == null ) {
		if ( typeof selector === "string" ) {

			// ( types, selector, fn )
			fn = data;
			data = undefined;
		} else {

			// ( types, data, fn )
			fn = data;
			data = selector;
			selector = undefined;
		}
	}
	if ( fn === false ) {
		fn = returnFalse;
	} else if ( !fn ) {
		return elem;
	}

	if ( one === 1 ) {
		origFn = fn;
		fn = function( event ) {

			// Can use an empty set, since event contains the info
			jQuery().off( event );
			return origFn.apply( this, arguments );
		};

		// Use same guid so caller can remove using origFn
		fn.guid = origFn.guid || ( origFn.guid = jQuery.guid++ );
	}
	return elem.each( function() {
		jQuery.event.add( this, types, fn, data, selector );
	} );
}

/*
 * Helper functions for managing events -- not part of the public interface.
 * Props to Dean Edwards' addEvent library for many of the ideas.
 */
jQuery.event = {

	global: {},

	add: function( elem, types, handler, data, selector ) {

		var handleObjIn, eventHandle, tmp,
			events, t, handleObj,
			special, handlers, type, namespaces, origType,
			elemData = dataPriv.get( elem );

		// Only attach events to objects that accept data
		if ( !acceptData( elem ) ) {
			return;
		}

		// Caller can pass in an object of custom data in lieu of the handler
		if ( handler.handler ) {
			handleObjIn = handler;
			handler = handleObjIn.handler;
			selector = handleObjIn.selector;
		}

		// Ensure that invalid selectors throw exceptions at attach time
		// Evaluate against documentElement in case elem is a non-element node (e.g., document)
		if ( selector ) {
			jQuery.find.matchesSelector( documentElement, selector );
		}

		// Make sure that the handler has a unique ID, used to find/remove it later
		if ( !handler.guid ) {
			handler.guid = jQuery.guid++;
		}

		// Init the element's event structure and main handler, if this is the first
		if ( !( events = elemData.events ) ) {
			events = elemData.events = Object.create( null );
		}
		if ( !( eventHandle = elemData.handle ) ) {
			eventHandle = elemData.handle = function( e ) {

				// Discard the second event of a jQuery.event.trigger() and
				// when an event is called after a page has unloaded
				return typeof jQuery !== "undefined" && jQuery.event.triggered !== e.type ?
					jQuery.event.dispatch.apply( elem, arguments ) : undefined;
			};
		}

		// Handle multiple events separated by a space
		types = ( types || "" ).match( rnothtmlwhite ) || [ "" ];
		t = types.length;
		while ( t-- ) {
			tmp = rtypenamespace.exec( types[ t ] ) || [];
			type = origType = tmp[ 1 ];
			namespaces = ( tmp[ 2 ] || "" ).split( "." ).sort();

			// There *must* be a type, no attaching namespace-only handlers
			if ( !type ) {
				continue;
			}

			// If event changes its type, use the special event handlers for the changed type
			special = jQuery.event.special[ type ] || {};

			// If selector defined, determine special event api type, otherwise given type
			type = ( selector ? special.delegateType : special.bindType ) || type;

			// Update special based on newly reset type
			special = jQuery.event.special[ type ] || {};

			// handleObj is passed to all event handlers
			handleObj = jQuery.extend( {
				type: type,
				origType: origType,
				data: data,
				handler: handler,
				guid: handler.guid,
				selector: selector,
				needsContext: selector && jQuery.expr.match.needsContext.test( selector ),
				namespace: namespaces.join( "." )
			}, handleObjIn );

			// Init the event handler queue if we're the first
			if ( !( handlers = events[ type ] ) ) {
				handlers = events[ type ] = [];
				handlers.delegateCount = 0;

				// Only use addEventListener if the special events handler returns false
				if ( !special.setup ||
					special.setup.call( elem, data, namespaces, eventHandle ) === false ) {

					if ( elem.addEventListener ) {
						elem.addEventListener( type, eventHandle );
					}
				}
			}

			if ( special.add ) {
				special.add.call( elem, handleObj );

				if ( !handleObj.handler.guid ) {
					handleObj.handler.guid = handler.guid;
				}
			}

			// Add to the element's handler list, delegates in front
			if ( selector ) {
				handlers.splice( handlers.delegateCount++, 0, handleObj );
			} else {
				handlers.push( handleObj );
			}

			// Keep track of which events have ever been used, for event optimization
			jQuery.event.global[ type ] = true;
		}

	},

	// Detach an event or set of events from an element
	remove: function( elem, types, handler, selector, mappedTypes ) {

		var j, origCount, tmp,
			events, t, handleObj,
			special, handlers, type, namespaces, origType,
			elemData = dataPriv.hasData( elem ) && dataPriv.get( elem );

		if ( !elemData || !( events = elemData.events ) ) {
			return;
		}

		// Once for each type.namespace in types; type may be omitted
		types = ( types || "" ).match( rnothtmlwhite ) || [ "" ];
		t = types.length;
		while ( t-- ) {
			tmp = rtypenamespace.exec( types[ t ] ) || [];
			type = origType = tmp[ 1 ];
			namespaces = ( tmp[ 2 ] || "" ).split( "." ).sort();

			// Unbind all events (on this namespace, if provided) for the element
			if ( !type ) {
				for ( type in events ) {
					jQuery.event.remove( elem, type + types[ t ], handler, selector, true );
				}
				continue;
			}

			special = jQuery.event.special[ type ] || {};
			type = ( selector ? special.delegateType : special.bindType ) || type;
			handlers = events[ type ] || [];
			tmp = tmp[ 2 ] &&
				new RegExp( "(^|\\.)" + namespaces.join( "\\.(?:.*\\.|)" ) + "(\\.|$)" );

			// Remove matching events
			origCount = j = handlers.length;
			while ( j-- ) {
				handleObj = handlers[ j ];

				if ( ( mappedTypes || origType === handleObj.origType ) &&
					( !handler || handler.guid === handleObj.guid ) &&
					( !tmp || tmp.test( handleObj.namespace ) ) &&
					( !selector || selector === handleObj.selector ||
						selector === "**" && handleObj.selector ) ) {
					handlers.splice( j, 1 );

					if ( handleObj.selector ) {
						handlers.delegateCount--;
					}
					if ( special.remove ) {
						special.remove.call( elem, handleObj );
					}
				}
			}

			// Remove generic event handler if we removed something and no more handlers exist
			// (avoids potential for endless recursion during removal of special event handlers)
			if ( origCount && !handlers.length ) {
				if ( !special.teardown ||
					special.teardown.call( elem, namespaces, elemData.handle ) === false ) {

					jQuery.removeEvent( elem, type, elemData.handle );
				}

				delete events[ type ];
			}
		}

		// Remove data and the expando if it's no longer used
		if ( jQuery.isEmptyObject( events ) ) {
			dataPriv.remove( elem, "handle events" );
		}
	},

	dispatch: function( nativeEvent ) {

		var i, j, ret, matched, handleObj, handlerQueue,
			args = new Array( arguments.length ),

			// Make a writable jQuery.Event from the native event object
			event = jQuery.event.fix( nativeEvent ),

			handlers = (
					dataPriv.get( this, "events" ) || Object.create( null )
				)[ event.type ] || [],
			special = jQuery.event.special[ event.type ] || {};

		// Use the fix-ed jQuery.Event rather than the (read-only) native event
		args[ 0 ] = event;

		for ( i = 1; i < arguments.length; i++ ) {
			args[ i ] = arguments[ i ];
		}

		event.delegateTarget = this;

		// Call the preDispatch hook for the mapped type, and let it bail if desired
		if ( special.preDispatch && special.preDispatch.call( this, event ) === false ) {
			return;
		}

		// Determine handlers
		handlerQueue = jQuery.event.handlers.call( this, event, handlers );

		// Run delegates first; they may want to stop propagation beneath us
		i = 0;
		while ( ( matched = handlerQueue[ i++ ] ) && !event.isPropagationStopped() ) {
			event.currentTarget = matched.elem;

			j = 0;
			while ( ( handleObj = matched.handlers[ j++ ] ) &&
				!event.isImmediatePropagationStopped() ) {

				// If the event is namespaced, then each handler is only invoked if it is
				// specially universal or its namespaces are a superset of the event's.
				if ( !event.rnamespace || handleObj.namespace === false ||
					event.rnamespace.test( handleObj.namespace ) ) {

					event.handleObj = handleObj;
					event.data = handleObj.data;

					ret = ( ( jQuery.event.special[ handleObj.origType ] || {} ).handle ||
						handleObj.handler ).apply( matched.elem, args );

					if ( ret !== undefined ) {
						if ( ( event.result = ret ) === false ) {
							event.preventDefault();
							event.stopPropagation();
						}
					}
				}
			}
		}

		// Call the postDispatch hook for the mapped type
		if ( special.postDispatch ) {
			special.postDispatch.call( this, event );
		}

		return event.result;
	},

	handlers: function( event, handlers ) {
		var i, handleObj, sel, matchedHandlers, matchedSelectors,
			handlerQueue = [],
			delegateCount = handlers.delegateCount,
			cur = event.target;

		// Find delegate handlers
		if ( delegateCount &&

			// Support: IE <=9
			// Black-hole SVG <use> instance trees (trac-13180)
			cur.nodeType &&

			// Support: Firefox <=42
			// Suppress spec-violating clicks indicating a non-primary pointer button (trac-3861)
			// https://www.w3.org/TR/DOM-Level-3-Events/#event-type-click
			// Support: IE 11 only
			// ...but not arrow key "clicks" of radio inputs, which can have `button` -1 (gh-2343)
			!( event.type === "click" && event.button >= 1 ) ) {

			for ( ; cur !== this; cur = cur.parentNode || this ) {

				// Don't check non-elements (#13208)
				// Don't process clicks on disabled elements (#6911, #8165, #11382, #11764)
				if ( cur.nodeType === 1 && !( event.type === "click" && cur.disabled === true ) ) {
					matchedHandlers = [];
					matchedSelectors = {};
					for ( i = 0; i < delegateCount; i++ ) {
						handleObj = handlers[ i ];

						// Don't conflict with Object.prototype properties (#13203)
						sel = handleObj.selector + " ";

						if ( matchedSelectors[ sel ] === undefined ) {
							matchedSelectors[ sel ] = handleObj.needsContext ?
								jQuery( sel, this ).index( cur ) > -1 :
								jQuery.find( sel, this, null, [ cur ] ).length;
						}
						if ( matchedSelectors[ sel ] ) {
							matchedHandlers.push( handleObj );
						}
					}
					if ( matchedHandlers.length ) {
						handlerQueue.push( { elem: cur, handlers: matchedHandlers } );
					}
				}
			}
		}

		// Add the remaining (directly-bound) handlers
		cur = this;
		if ( delegateCount < handlers.length ) {
			handlerQueue.push( { elem: cur, handlers: handlers.slice( delegateCount ) } );
		}

		return handlerQueue;
	},

	addProp: function( name, hook ) {
		Object.defineProperty( jQuery.Event.prototype, name, {
			enumerable: true,
			configurable: true,

			get: isFunction( hook ) ?
				function() {
					if ( this.originalEvent ) {
							return hook( this.originalEvent );
					}
				} :
				function() {
					if ( this.originalEvent ) {
							return this.originalEvent[ name ];
					}
				},

			set: function( value ) {
				Object.defineProperty( this, name, {
					enumerable: true,
					configurable: true,
					writable: true,
					value: value
				} );
			}
		} );
	},

	fix: function( originalEvent ) {
		return originalEvent[ jQuery.expando ] ?
			originalEvent :
			new jQuery.Event( originalEvent );
	},

	special: {
		load: {

			// Prevent triggered image.load events from bubbling to window.load
			noBubble: true
		},
		click: {

			// Utilize native event to ensure correct state for checkable inputs
			setup: function( data ) {

				// For mutual compressibility with _default, replace `this` access with a local var.
				// `|| data` is dead code meant only to preserve the variable through minification.
				var el = this || data;

				// Claim the first handler
				if ( rcheckableType.test( el.type ) &&
					el.click && nodeName( el, "input" ) ) {

					// dataPriv.set( el, "click", ... )
					leverageNative( el, "click", returnTrue );
				}

				// Return false to allow normal processing in the caller
				return false;
			},
			trigger: function( data ) {

				// For mutual compressibility with _default, replace `this` access with a local var.
				// `|| data` is dead code meant only to preserve the variable through minification.
				var el = this || data;

				// Force setup before triggering a click
				if ( rcheckableType.test( el.type ) &&
					el.click && nodeName( el, "input" ) ) {

					leverageNative( el, "click" );
				}

				// Return non-false to allow normal event-path propagation
				return true;
			},

			// For cross-browser consistency, suppress native .click() on links
			// Also prevent it if we're currently inside a leveraged native-event stack
			_default: function( event ) {
				var target = event.target;
				return rcheckableType.test( target.type ) &&
					target.click && nodeName( target, "input" ) &&
					dataPriv.get( target, "click" ) ||
					nodeName( target, "a" );
			}
		},

		beforeunload: {
			postDispatch: function( event ) {

				// Support: Firefox 20+
				// Firefox doesn't alert if the returnValue field is not set.
				if ( event.result !== undefined && event.originalEvent ) {
					event.originalEvent.returnValue = event.result;
				}
			}
		}
	}
};

// Ensure the presence of an event listener that handles manually-triggered
// synthetic events by interrupting progress until reinvoked in response to
// *native* events that it fires directly, ensuring that state changes have
// already occurred before other listeners are invoked.
function leverageNative( el, type, expectSync ) {

	// Missing expectSync indicates a trigger call, which must force setup through jQuery.event.add
	if ( !expectSync ) {
		if ( dataPriv.get( el, type ) === undefined ) {
			jQuery.event.add( el, type, returnTrue );
		}
		return;
	}

	// Register the controller as a special universal handler for all event namespaces
	dataPriv.set( el, type, false );
	jQuery.event.add( el, type, {
		namespace: false,
		handler: function( event ) {
			var notAsync, result,
				saved = dataPriv.get( this, type );

			if ( ( event.isTrigger & 1 ) && this[ type ] ) {

				// Interrupt processing of the outer synthetic .trigger()ed event
				// Saved data should be false in such cases, but might be a leftover capture object
				// from an async native handler (gh-4350)
				if ( !saved.length ) {

					// Store arguments for use when handling the inner native event
					// There will always be at least one argument (an event object), so this array
					// will not be confused with a leftover capture object.
					saved = slice.call( arguments );
					dataPriv.set( this, type, saved );

					// Trigger the native event and capture its result
					// Support: IE <=9 - 11+
					// focus() and blur() are asynchronous
					notAsync = expectSync( this, type );
					this[ type ]();
					result = dataPriv.get( this, type );
					if ( saved !== result || notAsync ) {
						dataPriv.set( this, type, false );
					} else {
						result = {};
					}
					if ( saved !== result ) {

						// Cancel the outer synthetic event
						event.stopImmediatePropagation();
						event.preventDefault();
						return result.value;
					}

				// If this is an inner synthetic event for an event with a bubbling surrogate
				// (focus or blur), assume that the surrogate already propagated from triggering the
				// native event and prevent that from happening again here.
				// This technically gets the ordering wrong w.r.t. to `.trigger()` (in which the
				// bubbling surrogate propagates *after* the non-bubbling base), but that seems
				// less bad than duplication.
				} else if ( ( jQuery.event.special[ type ] || {} ).delegateType ) {
					event.stopPropagation();
				}

			// If this is a native event triggered above, everything is now in order
			// Fire an inner synthetic event with the original arguments
			} else if ( saved.length ) {

				// ...and capture the result
				dataPriv.set( this, type, {
					value: jQuery.event.trigger(

						// Support: IE <=9 - 11+
						// Extend with the prototype to reset the above stopImmediatePropagation()
						jQuery.extend( saved[ 0 ], jQuery.Event.prototype ),
						saved.slice( 1 ),
						this
					)
				} );

				// Abort handling of the native event
				event.stopImmediatePropagation();
			}
		}
	} );
}

jQuery.removeEvent = function( elem, type, handle ) {

	// This "if" is needed for plain objects
	if ( elem.removeEventListener ) {
		elem.removeEventListener( type, handle );
	}
};

jQuery.Event = function( src, props ) {

	// Allow instantiation without the 'new' keyword
	if ( !( this instanceof jQuery.Event ) ) {
		return new jQuery.Event( src, props );
	}

	// Event object
	if ( src && src.type ) {
		this.originalEvent = src;
		this.type = src.type;

		// Events bubbling up the document may have been marked as prevented
		// by a handler lower down the tree; reflect the correct value.
		this.isDefaultPrevented = src.defaultPrevented ||
				src.defaultPrevented === undefined &&

				// Support: Android <=2.3 only
				src.returnValue === false ?
			returnTrue :
			returnFalse;

		// Create target properties
		// Support: Safari <=6 - 7 only
		// Target should not be a text node (#504, #13143)
		this.target = ( src.target && src.target.nodeType === 3 ) ?
			src.target.parentNode :
			src.target;

		this.currentTarget = src.currentTarget;
		this.relatedTarget = src.relatedTarget;

	// Event type
	} else {
		this.type = src;
	}

	// Put explicitly provided properties onto the event object
	if ( props ) {
		jQuery.extend( this, props );
	}

	// Create a timestamp if incoming event doesn't have one
	this.timeStamp = src && src.timeStamp || Date.now();

	// Mark it as fixed
	this[ jQuery.expando ] = true;
};

// jQuery.Event is based on DOM3 Events as specified by the ECMAScript Language Binding
// https://www.w3.org/TR/2003/WD-DOM-Level-3-Events-20030331/ecma-script-binding.html
jQuery.Event.prototype = {
	constructor: jQuery.Event,
	isDefaultPrevented: returnFalse,
	isPropagationStopped: returnFalse,
	isImmediatePropagationStopped: returnFalse,
	isSimulated: false,

	preventDefault: function() {
		var e = this.originalEvent;

		this.isDefaultPrevented = returnTrue;

		if ( e && !this.isSimulated ) {
			e.preventDefault();
		}
	},
	stopPropagation: function() {
		var e = this.originalEvent;

		this.isPropagationStopped = returnTrue;

		if ( e && !this.isSimulated ) {
			e.stopPropagation();
		}
	},
	stopImmediatePropagation: function() {
		var e = this.originalEvent;

		this.isImmediatePropagationStopped = returnTrue;

		if ( e && !this.isSimulated ) {
			e.stopImmediatePropagation();
		}

		this.stopPropagation();
	}
};

// Includes all common event props including KeyEvent and MouseEvent specific props
jQuery.each( {
	altKey: true,
	bubbles: true,
	cancelable: true,
	changedTouches: true,
	ctrlKey: true,
	detail: true,
	eventPhase: true,
	metaKey: true,
	pageX: true,
	pageY: true,
	shiftKey: true,
	view: true,
	"char": true,
	code: true,
	charCode: true,
	key: true,
	keyCode: true,
	button: true,
	buttons: true,
	clientX: true,
	clientY: true,
	offsetX: true,
	offsetY: true,
	pointerId: true,
	pointerType: true,
	screenX: true,
	screenY: true,
	targetTouches: true,
	toElement: true,
	touches: true,

	which: function( event ) {
		var button = event.button;

		// Add which for key events
		if ( event.which == null && rkeyEvent.test( event.type ) ) {
			return event.charCode != null ? event.charCode : event.keyCode;
		}

		// Add which for click: 1 === left; 2 === middle; 3 === right
		if ( !event.which && button !== undefined && rmouseEvent.test( event.type ) ) {
			if ( button & 1 ) {
				return 1;
			}

			if ( button & 2 ) {
				return 3;
			}

			if ( button & 4 ) {
				return 2;
			}

			return 0;
		}

		return event.which;
	}
}, jQuery.event.addProp );

jQuery.each( { focus: "focusin", blur: "focusout" }, function( type, delegateType ) {
	jQuery.event.special[ type ] = {

		// Utilize native event if possible so blur/focus sequence is correct
		setup: function() {

			// Claim the first handler
			// dataPriv.set( this, "focus", ... )
			// dataPriv.set( this, "blur", ... )
			leverageNative( this, type, expectSync );

			// Return false to allow normal processing in the caller
			return false;
		},
		trigger: function() {

			// Force setup before trigger
			leverageNative( this, type );

			// Return non-false to allow normal event-path propagation
			return true;
		},

		delegateType: delegateType
	};
} );

// Create mouseenter/leave events using mouseover/out and event-time checks
// so that event delegation works in jQuery.
// Do the same for pointerenter/pointerleave and pointerover/pointerout
//
// Support: Safari 7 only
// Safari sends mouseenter too often; see:
// https://bugs.chromium.org/p/chromium/issues/detail?id=470258
// for the description of the bug (it existed in older Chrome versions as well).
jQuery.each( {
	mouseenter: "mouseover",
	mouseleave: "mouseout",
	pointerenter: "pointerover",
	pointerleave: "pointerout"
}, function( orig, fix ) {
	jQuery.event.special[ orig ] = {
		delegateType: fix,
		bindType: fix,

		handle: function( event ) {
			var ret,
				target = this,
				related = event.relatedTarget,
				handleObj = event.handleObj;

			// For mouseenter/leave call the handler if related is outside the target.
			// NB: No relatedTarget if the mouse left/entered the browser window
			if ( !related || ( related !== target && !jQuery.contains( target, related ) ) ) {
				event.type = handleObj.origType;
				ret = handleObj.handler.apply( this, arguments );
				event.type = fix;
			}
			return ret;
		}
	};
} );

jQuery.fn.extend( {

	on: function( types, selector, data, fn ) {
		return on( this, types, selector, data, fn );
	},
	one: function( types, selector, data, fn ) {
		return on( this, types, selector, data, fn, 1 );
	},
	off: function( types, selector, fn ) {
		var handleObj, type;
		if ( types && types.preventDefault && types.handleObj ) {

			// ( event )  dispatched jQuery.Event
			handleObj = types.handleObj;
			jQuery( types.delegateTarget ).off(
				handleObj.namespace ?
					handleObj.origType + "." + handleObj.namespace :
					handleObj.origType,
				handleObj.selector,
				handleObj.handler
			);
			return this;
		}
		if ( typeof types === "object" ) {

			// ( types-object [, selector] )
			for ( type in types ) {
				this.off( type, selector, types[ type ] );
			}
			return this;
		}
		if ( selector === false || typeof selector === "function" ) {

			// ( types [, fn] )
			fn = selector;
			selector = undefined;
		}
		if ( fn === false ) {
			fn = returnFalse;
		}
		return this.each( function() {
			jQuery.event.remove( this, types, fn, selector );
		} );
	}
} );


var

	// Support: IE <=10 - 11, Edge 12 - 13 only
	// In IE/Edge using regex groups here causes severe slowdowns.
	// See https://connect.microsoft.com/IE/feedback/details/1736512/
	rnoInnerhtml = /<script|<style|<link/i,

	// checked="checked" or checked
	rchecked = /checked\s*(?:[^=]|=\s*.checked.)/i,
	rcleanScript = /^\s*<!(?:\[CDATA\[|--)|(?:\]\]|--)>\s*$/g;

// Prefer a tbody over its parent table for containing new rows
function manipulationTarget( elem, content ) {
	if ( nodeName( elem, "table" ) &&
		nodeName( content.nodeType !== 11 ? content : content.firstChild, "tr" ) ) {

		return jQuery( elem ).children( "tbody" )[ 0 ] || elem;
	}

	return elem;
}

// Replace/restore the type attribute of script elements for safe DOM manipulation
function disableScript( elem ) {
	elem.type = ( elem.getAttribute( "type" ) !== null ) + "/" + elem.type;
	return elem;
}
function restoreScript( elem ) {
	if ( ( elem.type || "" ).slice( 0, 5 ) === "true/" ) {
		elem.type = elem.type.slice( 5 );
	} else {
		elem.removeAttribute( "type" );
	}

	return elem;
}

function cloneCopyEvent( src, dest ) {
	var i, l, type, pdataOld, udataOld, udataCur, events;

	if ( dest.nodeType !== 1 ) {
		return;
	}

	// 1. Copy private data: events, handlers, etc.
	if ( dataPriv.hasData( src ) ) {
		pdataOld = dataPriv.get( src );
		events = pdataOld.events;

		if ( events ) {
			dataPriv.remove( dest, "handle events" );

			for ( type in events ) {
				for ( i = 0, l = events[ type ].length; i < l; i++ ) {
					jQuery.event.add( dest, type, events[ type ][ i ] );
				}
			}
		}
	}

	// 2. Copy user data
	if ( dataUser.hasData( src ) ) {
		udataOld = dataUser.access( src );
		udataCur = jQuery.extend( {}, udataOld );

		dataUser.set( dest, udataCur );
	}
}

// Fix IE bugs, see support tests
function fixInput( src, dest ) {
	var nodeName = dest.nodeName.toLowerCase();

	// Fails to persist the checked state of a cloned checkbox or radio button.
	if ( nodeName === "input" && rcheckableType.test( src.type ) ) {
		dest.checked = src.checked;

	// Fails to return the selected option to the default selected state when cloning options
	} else if ( nodeName === "input" || nodeName === "textarea" ) {
		dest.defaultValue = src.defaultValue;
	}
}

function domManip( collection, args, callback, ignored ) {

	// Flatten any nested arrays
	args = flat( args );

	var fragment, first, scripts, hasScripts, node, doc,
		i = 0,
		l = collection.length,
		iNoClone = l - 1,
		value = args[ 0 ],
		valueIsFunction = isFunction( value );

	// We can't cloneNode fragments that contain checked, in WebKit
	if ( valueIsFunction ||
			( l > 1 && typeof value === "string" &&
				!support.checkClone && rchecked.test( value ) ) ) {
		return collection.each( function( index ) {
			var self = collection.eq( index );
			if ( valueIsFunction ) {
				args[ 0 ] = value.call( this, index, self.html() );
			}
			domManip( self, args, callback, ignored );
		} );
	}

	if ( l ) {
		fragment = buildFragment( args, collection[ 0 ].ownerDocument, false, collection, ignored );
		first = fragment.firstChild;

		if ( fragment.childNodes.length === 1 ) {
			fragment = first;
		}

		// Require either new content or an interest in ignored elements to invoke the callback
		if ( first || ignored ) {
			scripts = jQuery.map( getAll( fragment, "script" ), disableScript );
			hasScripts = scripts.length;

			// Use the original fragment for the last item
			// instead of the first because it can end up
			// being emptied incorrectly in certain situations (#8070).
			for ( ; i < l; i++ ) {
				node = fragment;

				if ( i !== iNoClone ) {
					node = jQuery.clone( node, true, true );

					// Keep references to cloned scripts for later restoration
					if ( hasScripts ) {

						// Support: Android <=4.0 only, PhantomJS 1 only
						// push.apply(_, arraylike) throws on ancient WebKit
						jQuery.merge( scripts, getAll( node, "script" ) );
					}
				}

				callback.call( collection[ i ], node, i );
			}

			if ( hasScripts ) {
				doc = scripts[ scripts.length - 1 ].ownerDocument;

				// Reenable scripts
				jQuery.map( scripts, restoreScript );

				// Evaluate executable scripts on first document insertion
				for ( i = 0; i < hasScripts; i++ ) {
					node = scripts[ i ];
					if ( rscriptType.test( node.type || "" ) &&
						!dataPriv.access( node, "globalEval" ) &&
						jQuery.contains( doc, node ) ) {

						if ( node.src && ( node.type || "" ).toLowerCase()  !== "module" ) {

							// Optional AJAX dependency, but won't run scripts if not present
							if ( jQuery._evalUrl && !node.noModule ) {
								jQuery._evalUrl( node.src, {
									nonce: node.nonce || node.getAttribute( "nonce" )
								}, doc );
							}
						} else {
							DOMEval( node.textContent.replace( rcleanScript, "" ), node, doc );
						}
					}
				}
			}
		}
	}

	return collection;
}

function remove( elem, selector, keepData ) {
	var node,
		nodes = selector ? jQuery.filter( selector, elem ) : elem,
		i = 0;

	for ( ; ( node = nodes[ i ] ) != null; i++ ) {
		if ( !keepData && node.nodeType === 1 ) {
			jQuery.cleanData( getAll( node ) );
		}

		if ( node.parentNode ) {
			if ( keepData && isAttached( node ) ) {
				setGlobalEval( getAll( node, "script" ) );
			}
			node.parentNode.removeChild( node );
		}
	}

	return elem;
}

jQuery.extend( {
	htmlPrefilter: function( html ) {
		return html;
	},

	clone: function( elem, dataAndEvents, deepDataAndEvents ) {
		var i, l, srcElements, destElements,
			clone = elem.cloneNode( true ),
			inPage = isAttached( elem );

		// Fix IE cloning issues
		if ( !support.noCloneChecked && ( elem.nodeType === 1 || elem.nodeType === 11 ) &&
				!jQuery.isXMLDoc( elem ) ) {

			// We eschew Sizzle here for performance reasons: https://jsperf.com/getall-vs-sizzle/2
			destElements = getAll( clone );
			srcElements = getAll( elem );

			for ( i = 0, l = srcElements.length; i < l; i++ ) {
				fixInput( srcElements[ i ], destElements[ i ] );
			}
		}

		// Copy the events from the original to the clone
		if ( dataAndEvents ) {
			if ( deepDataAndEvents ) {
				srcElements = srcElements || getAll( elem );
				destElements = destElements || getAll( clone );

				for ( i = 0, l = srcElements.length; i < l; i++ ) {
					cloneCopyEvent( srcElements[ i ], destElements[ i ] );
				}
			} else {
				cloneCopyEvent( elem, clone );
			}
		}

		// Preserve script evaluation history
		destElements = getAll( clone, "script" );
		if ( destElements.length > 0 ) {
			setGlobalEval( destElements, !inPage && getAll( elem, "script" ) );
		}

		// Return the cloned set
		return clone;
	},

	cleanData: function( elems ) {
		var data, elem, type,
			special = jQuery.event.special,
			i = 0;

		for ( ; ( elem = elems[ i ] ) !== undefined; i++ ) {
			if ( acceptData( elem ) ) {
				if ( ( data = elem[ dataPriv.expando ] ) ) {
					if ( data.events ) {
						for ( type in data.events ) {
							if ( special[ type ] ) {
								jQuery.event.remove( elem, type );

							// This is a shortcut to avoid jQuery.event.remove's overhead
							} else {
								jQuery.removeEvent( elem, type, data.handle );
							}
						}
					}

					// Support: Chrome <=35 - 45+
					// Assign undefined instead of using delete, see Data#remove
					elem[ dataPriv.expando ] = undefined;
				}
				if ( elem[ dataUser.expando ] ) {

					// Support: Chrome <=35 - 45+
					// Assign undefined instead of using delete, see Data#remove
					elem[ dataUser.expando ] = undefined;
				}
			}
		}
	}
} );

jQuery.fn.extend( {
	detach: function( selector ) {
		return remove( this, selector, true );
	},

	remove: function( selector ) {
		return remove( this, selector );
	},

	text: function( value ) {
		return access( this, function( value ) {
			return value === undefined ?
				jQuery.text( this ) :
				this.empty().each( function() {
					if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
						this.textContent = value;
					}
				} );
		}, null, value, arguments.length );
	},

	append: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
				var target = manipulationTarget( this, elem );
				target.appendChild( elem );
			}
		} );
	},

	prepend: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.nodeType === 1 || this.nodeType === 11 || this.nodeType === 9 ) {
				var target = manipulationTarget( this, elem );
				target.insertBefore( elem, target.firstChild );
			}
		} );
	},

	before: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.parentNode ) {
				this.parentNode.insertBefore( elem, this );
			}
		} );
	},

	after: function() {
		return domManip( this, arguments, function( elem ) {
			if ( this.parentNode ) {
				this.parentNode.insertBefore( elem, this.nextSibling );
			}
		} );
	},

	empty: function() {
		var elem,
			i = 0;

		for ( ; ( elem = this[ i ] ) != null; i++ ) {
			if ( elem.nodeType === 1 ) {

				// Prevent memory leaks
				jQuery.cleanData( getAll( elem, false ) );

				// Remove any remaining nodes
				elem.textContent = "";
			}
		}

		return this;
	},

	clone: function( dataAndEvents, deepDataAndEvents ) {
		dataAndEvents = dataAndEvents == null ? false : dataAndEvents;
		deepDataAndEvents = deepDataAndEvents == null ? dataAndEvents : deepDataAndEvents;

		return this.map( function() {
			return jQuery.clone( this, dataAndEvents, deepDataAndEvents );
		} );
	},

	html: function( value ) {
		return access( this, function( value ) {
			var elem = this[ 0 ] || {},
				i = 0,
				l = this.length;

			if ( value === undefined && elem.nodeType === 1 ) {
				return elem.innerHTML;
			}

			// See if we can take a shortcut and just use innerHTML
			if ( typeof value === "string" && !rnoInnerhtml.test( value ) &&
				!wrapMap[ ( rtagName.exec( value ) || [ "", "" ] )[ 1 ].toLowerCase() ] ) {

				value = jQuery.htmlPrefilter( value );

				try {
					for ( ; i < l; i++ ) {
						elem = this[ i ] || {};

						// Remove element nodes and prevent memory leaks
						if ( elem.nodeType === 1 ) {
							jQuery.cleanData( getAll( elem, false ) );
							elem.innerHTML = value;
						}
					}

					elem = 0;

				// If using innerHTML throws an exception, use the fallback method
				} catch ( e ) {}
			}

			if ( elem ) {
				this.empty().append( value );
			}
		}, null, value, arguments.length );
	},

	replaceWith: function() {
		var ignored = [];

		// Make the changes, replacing each non-ignored context element with the new content
		return domManip( this, arguments, function( elem ) {
			var parent = this.parentNode;

			if ( jQuery.inArray( this, ignored ) < 0 ) {
				jQuery.cleanData( getAll( this ) );
				if ( parent ) {
					parent.replaceChild( elem, this );
				}
			}

		// Force callback invocation
		}, ignored );
	}
} );

jQuery.each( {
	appendTo: "append",
	prependTo: "prepend",
	insertBefore: "before",
	insertAfter: "after",
	replaceAll: "replaceWith"
}, function( name, original ) {
	jQuery.fn[ name ] = function( selector ) {
		var elems,
			ret = [],
			insert = jQuery( selector ),
			last = insert.length - 1,
			i = 0;

		for ( ; i <= last; i++ ) {
			elems = i === last ? this : this.clone( true );
			jQuery( insert[ i ] )[ original ]( elems );

			// Support: Android <=4.0 only, PhantomJS 1 only
			// .get() because push.apply(_, arraylike) throws on ancient WebKit
			push.apply( ret, elems.get() );
		}

		return this.pushStack( ret );
	};
} );
var rnumnonpx = new RegExp( "^(" + pnum + ")(?!px)[a-z%]+$", "i" );

var getStyles = function( elem ) {

		// Support: IE <=11 only, Firefox <=30 (#15098, #14150)
		// IE throws on elements created in popups
		// FF meanwhile throws on frame elements through "defaultView.getComputedStyle"
		var view = elem.ownerDocument.defaultView;

		if ( !view || !view.opener ) {
			view = window;
		}

		return view.getComputedStyle( elem );
	};

var swap = function( elem, options, callback ) {
	var ret, name,
		old = {};

	// Remember the old values, and insert the new ones
	for ( name in options ) {
		old[ name ] = elem.style[ name ];
		elem.style[ name ] = options[ name ];
	}

	ret = callback.call( elem );

	// Revert the old values
	for ( name in options ) {
		elem.style[ name ] = old[ name ];
	}

	return ret;
};


var rboxStyle = new RegExp( cssExpand.join( "|" ), "i" );



( function() {

	// Executing both pixelPosition & boxSizingReliable tests require only one layout
	// so they're executed at the same time to save the second computation.
	function computeStyleTests() {

		// This is a singleton, we need to execute it only once
		if ( !div ) {
			return;
		}

		container.style.cssText = "position:absolute;left:-11111px;width:60px;" +
			"margin-top:1px;padding:0;border:0";
		div.style.cssText =
			"position:relative;display:block;box-sizing:border-box;overflow:scroll;" +
			"margin:auto;border:1px;padding:1px;" +
			"width:60%;top:1%";
		documentElement.appendChild( container ).appendChild( div );

		var divStyle = window.getComputedStyle( div );
		pixelPositionVal = divStyle.top !== "1%";

		// Support: Android 4.0 - 4.3 only, Firefox <=3 - 44
		reliableMarginLeftVal = roundPixelMeasures( divStyle.marginLeft ) === 12;

		// Support: Android 4.0 - 4.3 only, Safari <=9.1 - 10.1, iOS <=7.0 - 9.3
		// Some styles come back with percentage values, even though they shouldn't
		div.style.right = "60%";
		pixelBoxStylesVal = roundPixelMeasures( divStyle.right ) === 36;

		// Support: IE 9 - 11 only
		// Detect misreporting of content dimensions for box-sizing:border-box elements
		boxSizingReliableVal = roundPixelMeasures( divStyle.width ) === 36;

		// Support: IE 9 only
		// Detect overflow:scroll screwiness (gh-3699)
		// Support: Chrome <=64
		// Don't get tricked when zoom affects offsetWidth (gh-4029)
		div.style.position = "absolute";
		scrollboxSizeVal = roundPixelMeasures( div.offsetWidth / 3 ) === 12;

		documentElement.removeChild( container );

		// Nullify the div so it wouldn't be stored in the memory and
		// it will also be a sign that checks already performed
		div = null;
	}

	function roundPixelMeasures( measure ) {
		return Math.round( parseFloat( measure ) );
	}

	var pixelPositionVal, boxSizingReliableVal, scrollboxSizeVal, pixelBoxStylesVal,
		reliableTrDimensionsVal, reliableMarginLeftVal,
		container = document.createElement( "div" ),
		div = document.createElement( "div" );

	// Finish early in limited (non-browser) environments
	if ( !div.style ) {
		return;
	}

	// Support: IE <=9 - 11 only
	// Style of cloned element affects source element cloned (#8908)
	div.style.backgroundClip = "content-box";
	div.cloneNode( true ).style.backgroundClip = "";
	support.clearCloneStyle = div.style.backgroundClip === "content-box";

	jQuery.extend( support, {
		boxSizingReliable: function() {
			computeStyleTests();
			return boxSizingReliableVal;
		},
		pixelBoxStyles: function() {
			computeStyleTests();
			return pixelBoxStylesVal;
		},
		pixelPosition: function() {
			computeStyleTests();
			return pixelPositionVal;
		},
		reliableMarginLeft: function() {
			computeStyleTests();
			return reliableMarginLeftVal;
		},
		scrollboxSize: function() {
			computeStyleTests();
			return scrollboxSizeVal;
		},

		// Support: IE 9 - 11+, Edge 15 - 18+
		// IE/Edge misreport `getComputedStyle` of table rows with width/height
		// set in CSS while `offset*` properties report correct values.
		// Behavior in IE 9 is more subtle than in newer versions & it passes
		// some versions of this test; make sure not to make it pass there!
		reliableTrDimensions: function() {
			var table, tr, trChild, trStyle;
			if ( reliableTrDimensionsVal == null ) {
				table = document.createElement( "table" );
				tr = document.createElement( "tr" );
				trChild = document.createElement( "div" );

				table.style.cssText = "position:absolute;left:-11111px";
				tr.style.height = "1px";
				trChild.style.height = "9px";

				documentElement
					.appendChild( table )
					.appendChild( tr )
					.appendChild( trChild );

				trStyle = window.getComputedStyle( tr );
				reliableTrDimensionsVal = parseInt( trStyle.height ) > 3;

				documentElement.removeChild( table );
			}
			return reliableTrDimensionsVal;
		}
	} );
} )();


function curCSS( elem, name, computed ) {
	var width, minWidth, maxWidth, ret,

		// Support: Firefox 51+
		// Retrieving style before computed somehow
		// fixes an issue with getting wrong values
		// on detached elements
		style = elem.style;

	computed = computed || getStyles( elem );

	// getPropertyValue is needed for:
	//   .css('filter') (IE 9 only, #12537)
	//   .css('--customProperty) (#3144)
	if ( computed ) {
		ret = computed.getPropertyValue( name ) || computed[ name ];

		if ( ret === "" && !isAttached( elem ) ) {
			ret = jQuery.style( elem, name );
		}

		// A tribute to the "awesome hack by Dean Edwards"
		// Android Browser returns percentage for some values,
		// but width seems to be reliably pixels.
		// This is against the CSSOM draft spec:
		// https://drafts.csswg.org/cssom/#resolved-values
		if ( !support.pixelBoxStyles() && rnumnonpx.test( ret ) && rboxStyle.test( name ) ) {

			// Remember the original values
			width = style.width;
			minWidth = style.minWidth;
			maxWidth = style.maxWidth;

			// Put in the new values to get a computed value out
			style.minWidth = style.maxWidth = style.width = ret;
			ret = computed.width;

			// Revert the changed values
			style.width = width;
			style.minWidth = minWidth;
			style.maxWidth = maxWidth;
		}
	}

	return ret !== undefined ?

		// Support: IE <=9 - 11 only
		// IE returns zIndex value as an integer.
		ret + "" :
		ret;
}


function addGetHookIf( conditionFn, hookFn ) {

	// Define the hook, we'll check on the first run if it's really needed.
	return {
		get: function() {
			if ( conditionFn() ) {

				// Hook not needed (or it's not possible to use it due
				// to missing dependency), remove it.
				delete this.get;
				return;
			}

			// Hook needed; redefine it so that the support test is not executed again.
			return ( this.get = hookFn ).apply( this, arguments );
		}
	};
}


var cssPrefixes = [ "Webkit", "Moz", "ms" ],
	emptyStyle = document.createElement( "div" ).style,
	vendorProps = {};

// Return a vendor-prefixed property or undefined
function vendorPropName( name ) {

	// Check for vendor prefixed names
	var capName = name[ 0 ].toUpperCase() + name.slice( 1 ),
		i = cssPrefixes.length;

	while ( i-- ) {
		name = cssPrefixes[ i ] + capName;
		if ( name in emptyStyle ) {
			return name;
		}
	}
}

// Return a potentially-mapped jQuery.cssProps or vendor prefixed property
function finalPropName( name ) {
	var final = jQuery.cssProps[ name ] || vendorProps[ name ];

	if ( final ) {
		return final;
	}
	if ( name in emptyStyle ) {
		return name;
	}
	return vendorProps[ name ] = vendorPropName( name ) || name;
}


var

	// Swappable if display is none or starts with table
	// except "table", "table-cell", or "table-caption"
	// See here for display values: https://developer.mozilla.org/en-US/docs/CSS/display
	rdisplayswap = /^(none|table(?!-c[ea]).+)/,
	rcustomProp = /^--/,
	cssShow = { position: "absolute", visibility: "hidden", display: "block" },
	cssNormalTransform = {
		letterSpacing: "0",
		fontWeight: "400"
	};

function setPositiveNumber( _elem, value, subtract ) {

	// Any relative (+/-) values have already been
	// normalized at this point
	var matches = rcssNum.exec( value );
	return matches ?

		// Guard against undefined "subtract", e.g., when used as in cssHooks
		Math.max( 0, matches[ 2 ] - ( subtract || 0 ) ) + ( matches[ 3 ] || "px" ) :
		value;
}

function boxModelAdjustment( elem, dimension, box, isBorderBox, styles, computedVal ) {
	var i = dimension === "width" ? 1 : 0,
		extra = 0,
		delta = 0;

	// Adjustment may not be necessary
	if ( box === ( isBorderBox ? "border" : "content" ) ) {
		return 0;
	}

	for ( ; i < 4; i += 2 ) {

		// Both box models exclude margin
		if ( box === "margin" ) {
			delta += jQuery.css( elem, box + cssExpand[ i ], true, styles );
		}

		// If we get here with a content-box, we're seeking "padding" or "border" or "margin"
		if ( !isBorderBox ) {

			// Add padding
			delta += jQuery.css( elem, "padding" + cssExpand[ i ], true, styles );

			// For "border" or "margin", add border
			if ( box !== "padding" ) {
				delta += jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );

			// But still keep track of it otherwise
			} else {
				extra += jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );
			}

		// If we get here with a border-box (content + padding + border), we're seeking "content" or
		// "padding" or "margin"
		} else {

			// For "content", subtract padding
			if ( box === "content" ) {
				delta -= jQuery.css( elem, "padding" + cssExpand[ i ], true, styles );
			}

			// For "content" or "padding", subtract border
			if ( box !== "margin" ) {
				delta -= jQuery.css( elem, "border" + cssExpand[ i ] + "Width", true, styles );
			}
		}
	}

	// Account for positive content-box scroll gutter when requested by providing computedVal
	if ( !isBorderBox && computedVal >= 0 ) {

		// offsetWidth/offsetHeight is a rounded sum of content, padding, scroll gutter, and border
		// Assuming integer scroll gutter, subtract the rest and round down
		delta += Math.max( 0, Math.ceil(
			elem[ "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 ) ] -
			computedVal -
			delta -
			extra -
			0.5

		// If offsetWidth/offsetHeight is unknown, then we can't determine content-box scroll gutter
		// Use an explicit zero to avoid NaN (gh-3964)
		) ) || 0;
	}

	return delta;
}

function getWidthOrHeight( elem, dimension, extra ) {

	// Start with computed style
	var styles = getStyles( elem ),

		// To avoid forcing a reflow, only fetch boxSizing if we need it (gh-4322).
		// Fake content-box until we know it's needed to know the true value.
		boxSizingNeeded = !support.boxSizingReliable() || extra,
		isBorderBox = boxSizingNeeded &&
			jQuery.css( elem, "boxSizing", false, styles ) === "border-box",
		valueIsBorderBox = isBorderBox,

		val = curCSS( elem, dimension, styles ),
		offsetProp = "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 );

	// Support: Firefox <=54
	// Return a confounding non-pixel value or feign ignorance, as appropriate.
	if ( rnumnonpx.test( val ) ) {
		if ( !extra ) {
			return val;
		}
		val = "auto";
	}


	// Support: IE 9 - 11 only
	// Use offsetWidth/offsetHeight for when box sizing is unreliable.
	// In those cases, the computed value can be trusted to be border-box.
	if ( ( !support.boxSizingReliable() && isBorderBox ||

		// Support: IE 10 - 11+, Edge 15 - 18+
		// IE/Edge misreport `getComputedStyle` of table rows with width/height
		// set in CSS while `offset*` properties report correct values.
		// Interestingly, in some cases IE 9 doesn't suffer from this issue.
		!support.reliableTrDimensions() && nodeName( elem, "tr" ) ||

		// Fall back to offsetWidth/offsetHeight when value is "auto"
		// This happens for inline elements with no explicit setting (gh-3571)
		val === "auto" ||

		// Support: Android <=4.1 - 4.3 only
		// Also use offsetWidth/offsetHeight for misreported inline dimensions (gh-3602)
		!parseFloat( val ) && jQuery.css( elem, "display", false, styles ) === "inline" ) &&

		// Make sure the element is visible & connected
		elem.getClientRects().length ) {

		isBorderBox = jQuery.css( elem, "boxSizing", false, styles ) === "border-box";

		// Where available, offsetWidth/offsetHeight approximate border box dimensions.
		// Where not available (e.g., SVG), assume unreliable box-sizing and interpret the
		// retrieved value as a content box dimension.
		valueIsBorderBox = offsetProp in elem;
		if ( valueIsBorderBox ) {
			val = elem[ offsetProp ];
		}
	}

	// Normalize "" and auto
	val = parseFloat( val ) || 0;

	// Adjust for the element's box model
	return ( val +
		boxModelAdjustment(
			elem,
			dimension,
			extra || ( isBorderBox ? "border" : "content" ),
			valueIsBorderBox,
			styles,

			// Provide the current computed size to request scroll gutter calculation (gh-3589)
			val
		)
	) + "px";
}

jQuery.extend( {

	// Add in style property hooks for overriding the default
	// behavior of getting and setting a style property
	cssHooks: {
		opacity: {
			get: function( elem, computed ) {
				if ( computed ) {

					// We should always get a number back from opacity
					var ret = curCSS( elem, "opacity" );
					return ret === "" ? "1" : ret;
				}
			}
		}
	},

	// Don't automatically add "px" to these possibly-unitless properties
	cssNumber: {
		"animationIterationCount": true,
		"columnCount": true,
		"fillOpacity": true,
		"flexGrow": true,
		"flexShrink": true,
		"fontWeight": true,
		"gridArea": true,
		"gridColumn": true,
		"gridColumnEnd": true,
		"gridColumnStart": true,
		"gridRow": true,
		"gridRowEnd": true,
		"gridRowStart": true,
		"lineHeight": true,
		"opacity": true,
		"order": true,
		"orphans": true,
		"widows": true,
		"zIndex": true,
		"zoom": true
	},

	// Add in properties whose names you wish to fix before
	// setting or getting the value
	cssProps: {},

	// Get and set the style property on a DOM Node
	style: function( elem, name, value, extra ) {

		// Don't set styles on text and comment nodes
		if ( !elem || elem.nodeType === 3 || elem.nodeType === 8 || !elem.style ) {
			return;
		}

		// Make sure that we're working with the right name
		var ret, type, hooks,
			origName = camelCase( name ),
			isCustomProp = rcustomProp.test( name ),
			style = elem.style;

		// Make sure that we're working with the right name. We don't
		// want to query the value if it is a CSS custom property
		// since they are user-defined.
		if ( !isCustomProp ) {
			name = finalPropName( origName );
		}

		// Gets hook for the prefixed version, then unprefixed version
		hooks = jQuery.cssHooks[ name ] || jQuery.cssHooks[ origName ];

		// Check if we're setting a value
		if ( value !== undefined ) {
			type = typeof value;

			// Convert "+=" or "-=" to relative numbers (#7345)
			if ( type === "string" && ( ret = rcssNum.exec( value ) ) && ret[ 1 ] ) {
				value = adjustCSS( elem, name, ret );

				// Fixes bug #9237
				type = "number";
			}

			// Make sure that null and NaN values aren't set (#7116)
			if ( value == null || value !== value ) {
				return;
			}

			// If a number was passed in, add the unit (except for certain CSS properties)
			// The isCustomProp check can be removed in jQuery 4.0 when we only auto-append
			// "px" to a few hardcoded values.
			if ( type === "number" && !isCustomProp ) {
				value += ret && ret[ 3 ] || ( jQuery.cssNumber[ origName ] ? "" : "px" );
			}

			// background-* props affect original clone's values
			if ( !support.clearCloneStyle && value === "" && name.indexOf( "background" ) === 0 ) {
				style[ name ] = "inherit";
			}

			// If a hook was provided, use that value, otherwise just set the specified value
			if ( !hooks || !( "set" in hooks ) ||
				( value = hooks.set( elem, value, extra ) ) !== undefined ) {

				if ( isCustomProp ) {
					style.setProperty( name, value );
				} else {
					style[ name ] = value;
				}
			}

		} else {

			// If a hook was provided get the non-computed value from there
			if ( hooks && "get" in hooks &&
				( ret = hooks.get( elem, false, extra ) ) !== undefined ) {

				return ret;
			}

			// Otherwise just get the value from the style object
			return style[ name ];
		}
	},

	css: function( elem, name, extra, styles ) {
		var val, num, hooks,
			origName = camelCase( name ),
			isCustomProp = rcustomProp.test( name );

		// Make sure that we're working with the right name. We don't
		// want to modify the value if it is a CSS custom property
		// since they are user-defined.
		if ( !isCustomProp ) {
			name = finalPropName( origName );
		}

		// Try prefixed name followed by the unprefixed name
		hooks = jQuery.cssHooks[ name ] || jQuery.cssHooks[ origName ];

		// If a hook was provided get the computed value from there
		if ( hooks && "get" in hooks ) {
			val = hooks.get( elem, true, extra );
		}

		// Otherwise, if a way to get the computed value exists, use that
		if ( val === undefined ) {
			val = curCSS( elem, name, styles );
		}

		// Convert "normal" to computed value
		if ( val === "normal" && name in cssNormalTransform ) {
			val = cssNormalTransform[ name ];
		}

		// Make numeric if forced or a qualifier was provided and val looks numeric
		if ( extra === "" || extra ) {
			num = parseFloat( val );
			return extra === true || isFinite( num ) ? num || 0 : val;
		}

		return val;
	}
} );

jQuery.each( [ "height", "width" ], function( _i, dimension ) {
	jQuery.cssHooks[ dimension ] = {
		get: function( elem, computed, extra ) {
			if ( computed ) {

				// Certain elements can have dimension info if we invisibly show them
				// but it must have a current display style that would benefit
				return rdisplayswap.test( jQuery.css( elem, "display" ) ) &&

					// Support: Safari 8+
					// Table columns in Safari have non-zero offsetWidth & zero
					// getBoundingClientRect().width unless display is changed.
					// Support: IE <=11 only
					// Running getBoundingClientRect on a disconnected node
					// in IE throws an error.
					( !elem.getClientRects().length || !elem.getBoundingClientRect().width ) ?
						swap( elem, cssShow, function() {
							return getWidthOrHeight( elem, dimension, extra );
						} ) :
						getWidthOrHeight( elem, dimension, extra );
			}
		},

		set: function( elem, value, extra ) {
			var matches,
				styles = getStyles( elem ),

				// Only read styles.position if the test has a chance to fail
				// to avoid forcing a reflow.
				scrollboxSizeBuggy = !support.scrollboxSize() &&
					styles.position === "absolute",

				// To avoid forcing a reflow, only fetch boxSizing if we need it (gh-3991)
				boxSizingNeeded = scrollboxSizeBuggy || extra,
				isBorderBox = boxSizingNeeded &&
					jQuery.css( elem, "boxSizing", false, styles ) === "border-box",
				subtract = extra ?
					boxModelAdjustment(
						elem,
						dimension,
						extra,
						isBorderBox,
						styles
					) :
					0;

			// Account for unreliable border-box dimensions by comparing offset* to computed and
			// faking a content-box to get border and padding (gh-3699)
			if ( isBorderBox && scrollboxSizeBuggy ) {
				subtract -= Math.ceil(
					elem[ "offset" + dimension[ 0 ].toUpperCase() + dimension.slice( 1 ) ] -
					parseFloat( styles[ dimension ] ) -
					boxModelAdjustment( elem, dimension, "border", false, styles ) -
					0.5
				);
			}

			// Convert to pixels if value adjustment is needed
			if ( subtract && ( matches = rcssNum.exec( value ) ) &&
				( matches[ 3 ] || "px" ) !== "px" ) {

				elem.style[ dimension ] = value;
				value = jQuery.css( elem, dimension );
			}

			return setPositiveNumber( elem, value, subtract );
		}
	};
} );

jQuery.cssHooks.marginLeft = addGetHookIf( support.reliableMarginLeft,
	function( elem, computed ) {
		if ( computed ) {
			return ( parseFloat( curCSS( elem, "marginLeft" ) ) ||
				elem.getBoundingClientRect().left -
					swap( elem, { marginLeft: 0 }, function() {
						return elem.getBoundingClientRect().left;
					} )
				) + "px";
		}
	}
);

// These hooks are used by animate to expand properties
jQuery.each( {
	margin: "",
	padding: "",
	border: "Width"
}, function( prefix, suffix ) {
	jQuery.cssHooks[ prefix + suffix ] = {
		expand: function( value ) {
			var i = 0,
				expanded = {},

				// Assumes a single number if not a string
				parts = typeof value === "string" ? value.split( " " ) : [ value ];

			for ( ; i < 4; i++ ) {
				expanded[ prefix + cssExpand[ i ] + suffix ] =
					parts[ i ] || parts[ i - 2 ] || parts[ 0 ];
			}

			return expanded;
		}
	};

	if ( prefix !== "margin" ) {
		jQuery.cssHooks[ prefix + suffix ].set = setPositiveNumber;
	}
} );

jQuery.fn.extend( {
	css: function( name, value ) {
		return access( this, function( elem, name, value ) {
			var styles, len,
				map = {},
				i = 0;

			if ( Array.isArray( name ) ) {
				styles = getStyles( elem );
				len = name.length;

				for ( ; i < len; i++ ) {
					map[ name[ i ] ] = jQuery.css( elem, name[ i ], false, styles );
				}

				return map;
			}

			return value !== undefined ?
				jQuery.style( elem, name, value ) :
				jQuery.css( elem, name );
		}, name, value, arguments.length > 1 );
	}
} );


function Tween( elem, options, prop, end, easing ) {
	return new Tween.prototype.init( elem, options, prop, end, easing );
}
jQuery.Tween = Tween;

Tween.prototype = {
	constructor: Tween,
	init: function( elem, options, prop, end, easing, unit ) {
		this.elem = elem;
		this.prop = prop;
		this.easing = easing || jQuery.easing._default;
		this.options = options;
		this.start = this.now = this.cur();
		this.end = end;
		this.unit = unit || ( jQuery.cssNumber[ prop ] ? "" : "px" );
	},
	cur: function() {
		var hooks = Tween.propHooks[ this.prop ];

		return hooks && hooks.get ?
			hooks.get( this ) :
			Tween.propHooks._default.get( this );
	},
	run: function( percent ) {
		var eased,
			hooks = Tween.propHooks[ this.prop ];

		if ( this.options.duration ) {
			this.pos = eased = jQuery.easing[ this.easing ](
				percent, this.options.duration * percent, 0, 1, this.options.duration
			);
		} else {
			this.pos = eased = percent;
		}
		this.now = ( this.end - this.start ) * eased + this.start;

		if ( this.options.step ) {
			this.options.step.call( this.elem, this.now, this );
		}

		if ( hooks && hooks.set ) {
			hooks.set( this );
		} else {
			Tween.propHooks._default.set( this );
		}
		return this;
	}
};

Tween.prototype.init.prototype = Tween.prototype;

Tween.propHooks = {
	_default: {
		get: function( tween ) {
			var result;

			// Use a property on the element directly when it is not a DOM element,
			// or when there is no matching style property that exists.
			if ( tween.elem.nodeType !== 1 ||
				tween.elem[ tween.prop ] != null && tween.elem.style[ tween.prop ] == null ) {
				return tween.elem[ tween.prop ];
			}

			// Passing an empty string as a 3rd parameter to .css will automatically
			// attempt a parseFloat and fallback to a string if the parse fails.
			// Simple values such as "10px" are parsed to Float;
			// complex values such as "rotate(1rad)" are returned as-is.
			result = jQuery.css( tween.elem, tween.prop, "" );

			// Empty strings, null, undefined and "auto" are converted to 0.
			return !result || result === "auto" ? 0 : result;
		},
		set: function( tween ) {

			// Use step hook for back compat.
			// Use cssHook if its there.
			// Use .style if available and use plain properties where available.
			if ( jQuery.fx.step[ tween.prop ] ) {
				jQuery.fx.step[ tween.prop ]( tween );
			} else if ( tween.elem.nodeType === 1 && (
					jQuery.cssHooks[ tween.prop ] ||
					tween.elem.style[ finalPropName( tween.prop ) ] != null ) ) {
				jQuery.style( tween.elem, tween.prop, tween.now + tween.unit );
			} else {
				tween.elem[ tween.prop ] = tween.now;
			}
		}
	}
};

// Support: IE <=9 only
// Panic based approach to setting things on disconnected nodes
Tween.propHooks.scrollTop = Tween.propHooks.scrollLeft = {
	set: function( tween ) {
		if ( tween.elem.nodeType && tween.elem.parentNode ) {
			tween.elem[ tween.prop ] = tween.now;
		}
	}
};

jQuery.easing = {
	linear: function( p ) {
		return p;
	},
	swing: function( p ) {
		return 0.5 - Math.cos( p * Math.PI ) / 2;
	},
	_default: "swing"
};

jQuery.fx = Tween.prototype.init;

// Back compat <1.8 extension point
jQuery.fx.step = {};




var
	fxNow, inProgress,
	rfxtypes = /^(?:toggle|show|hide)$/,
	rrun = /queueHooks$/;

function schedule() {
	if ( inProgress ) {
		if ( document.hidden === false && window.requestAnimationFrame ) {
			window.requestAnimationFrame( schedule );
		} else {
			window.setTimeout( schedule, jQuery.fx.interval );
		}

		jQuery.fx.tick();
	}
}

// Animations created synchronously will run synchronously
function createFxNow() {
	window.setTimeout( function() {
		fxNow = undefined;
	} );
	return ( fxNow = Date.now() );
}

// Generate parameters to create a standard animation
function genFx( type, includeWidth ) {
	var which,
		i = 0,
		attrs = { height: type };

	// If we include width, step value is 1 to do all cssExpand values,
	// otherwise step value is 2 to skip over Left and Right
	includeWidth = includeWidth ? 1 : 0;
	for ( ; i < 4; i += 2 - includeWidth ) {
		which = cssExpand[ i ];
		attrs[ "margin" + which ] = attrs[ "padding" + which ] = type;
	}

	if ( includeWidth ) {
		attrs.opacity = attrs.width = type;
	}

	return attrs;
}

function createTween( value, prop, animation ) {
	var tween,
		collection = ( Animation.tweeners[ prop ] || [] ).concat( Animation.tweeners[ "*" ] ),
		index = 0,
		length = collection.length;
	for ( ; index < length; index++ ) {
		if ( ( tween = collection[ index ].call( animation, prop, value ) ) ) {

			// We're done with this property
			return tween;
		}
	}
}

function defaultPrefilter( elem, props, opts ) {
	var prop, value, toggle, hooks, oldfire, propTween, restoreDisplay, display,
		isBox = "width" in props || "height" in props,
		anim = this,
		orig = {},
		style = elem.style,
		hidden = elem.nodeType && isHiddenWithinTree( elem ),
		dataShow = dataPriv.get( elem, "fxshow" );

	// Queue-skipping animations hijack the fx hooks
	if ( !opts.queue ) {
		hooks = jQuery._queueHooks( elem, "fx" );
		if ( hooks.unqueued == null ) {
			hooks.unqueued = 0;
			oldfire = hooks.empty.fire;
			hooks.empty.fire = function() {
				if ( !hooks.unqueued ) {
					oldfire();
				}
			};
		}
		hooks.unqueued++;

		anim.always( function() {

			// Ensure the complete handler is called before this completes
			anim.always( function() {
				hooks.unqueued--;
				if ( !jQuery.queue( elem, "fx" ).length ) {
					hooks.empty.fire();
				}
			} );
		} );
	}

	// Detect show/hide animations
	for ( prop in props ) {
		value = props[ prop ];
		if ( rfxtypes.test( value ) ) {
			delete props[ prop ];
			toggle = toggle || value === "toggle";
			if ( value === ( hidden ? "hide" : "show" ) ) {

				// Pretend to be hidden if this is a "show" and
				// there is still data from a stopped show/hide
				if ( value === "show" && dataShow && dataShow[ prop ] !== undefined ) {
					hidden = true;

				// Ignore all other no-op show/hide data
				} else {
					continue;
				}
			}
			orig[ prop ] = dataShow && dataShow[ prop ] || jQuery.style( elem, prop );
		}
	}

	// Bail out if this is a no-op like .hide().hide()
	propTween = !jQuery.isEmptyObject( props );
	if ( !propTween && jQuery.isEmptyObject( orig ) ) {
		return;
	}

	// Restrict "overflow" and "display" styles during box animations
	if ( isBox && elem.nodeType === 1 ) {

		// Support: IE <=9 - 11, Edge 12 - 15
		// Record all 3 overflow attributes because IE does not infer the shorthand
		// from identically-valued overflowX and overflowY and Edge just mirrors
		// the overflowX value there.
		opts.overflow = [ style.overflow, style.overflowX, style.overflowY ];

		// Identify a display type, preferring old show/hide data over the CSS cascade
		restoreDisplay = dataShow && dataShow.display;
		if ( restoreDisplay == null ) {
			restoreDisplay = dataPriv.get( elem, "display" );
		}
		display = jQuery.css( elem, "display" );
		if ( display === "none" ) {
			if ( restoreDisplay ) {
				display = restoreDisplay;
			} else {

				// Get nonempty value(s) by temporarily forcing visibility
				showHide( [ elem ], true );
				restoreDisplay = elem.style.display || restoreDisplay;
				display = jQuery.css( elem, "display" );
				showHide( [ elem ] );
			}
		}

		// Animate inline elements as inline-block
		if ( display === "inline" || display === "inline-block" && restoreDisplay != null ) {
			if ( jQuery.css( elem, "float" ) === "none" ) {

				// Restore the original display value at the end of pure show/hide animations
				if ( !propTween ) {
					anim.done( function() {
						style.display = restoreDisplay;
					} );
					if ( restoreDisplay == null ) {
						display = style.display;
						restoreDisplay = display === "none" ? "" : display;
					}
				}
				style.display = "inline-block";
			}
		}
	}

	if ( opts.overflow ) {
		style.overflow = "hidden";
		anim.always( function() {
			style.overflow = opts.overflow[ 0 ];
			style.overflowX = opts.overflow[ 1 ];
			style.overflowY = opts.overflow[ 2 ];
		} );
	}

	// Implement show/hide animations
	propTween = false;
	for ( prop in orig ) {

		// General show/hide setup for this element animation
		if ( !propTween ) {
			if ( dataShow ) {
				if ( "hidden" in dataShow ) {
					hidden = dataShow.hidden;
				}
			} else {
				dataShow = dataPriv.access( elem, "fxshow", { display: restoreDisplay } );
			}

			// Store hidden/visible for toggle so `.stop().toggle()` "reverses"
			if ( toggle ) {
				dataShow.hidden = !hidden;
			}

			// Show elements before animating them
			if ( hidden ) {
				showHide( [ elem ], true );
			}

			/* eslint-disable no-loop-func */

			anim.done( function() {

			/* eslint-enable no-loop-func */

				// The final step of a "hide" animation is actually hiding the element
				if ( !hidden ) {
					showHide( [ elem ] );
				}
				dataPriv.remove( elem, "fxshow" );
				for ( prop in orig ) {
					jQuery.style( elem, prop, orig[ prop ] );
				}
			} );
		}

		// Per-property setup
		propTween = createTween( hidden ? dataShow[ prop ] : 0, prop, anim );
		if ( !( prop in dataShow ) ) {
			dataShow[ prop ] = propTween.start;
			if ( hidden ) {
				propTween.end = propTween.start;
				propTween.start = 0;
			}
		}
	}
}

function propFilter( props, specialEasing ) {
	var index, name, easing, value, hooks;

	// camelCase, specialEasing and expand cssHook pass
	for ( index in props ) {
		name = camelCase( index );
		easing = specialEasing[ name ];
		value = props[ index ];
		if ( Array.isArray( value ) ) {
			easing = value[ 1 ];
			value = props[ index ] = value[ 0 ];
		}

		if ( index !== name ) {
			props[ name ] = value;
			delete props[ index ];
		}

		hooks = jQuery.cssHooks[ name ];
		if ( hooks && "expand" in hooks ) {
			value = hooks.expand( value );
			delete props[ name ];

			// Not quite $.extend, this won't overwrite existing keys.
			// Reusing 'index' because we have the correct "name"
			for ( index in value ) {
				if ( !( index in props ) ) {
					props[ index ] = value[ index ];
					specialEasing[ index ] = easing;
				}
			}
		} else {
			specialEasing[ name ] = easing;
		}
	}
}

function Animation( elem, properties, options ) {
	var result,
		stopped,
		index = 0,
		length = Animation.prefilters.length,
		deferred = jQuery.Deferred().always( function() {

			// Don't match elem in the :animated selector
			delete tick.elem;
		} ),
		tick = function() {
			if ( stopped ) {
				return false;
			}
			var currentTime = fxNow || createFxNow(),
				remaining = Math.max( 0, animation.startTime + animation.duration - currentTime ),

				// Support: Android 2.3 only
				// Archaic crash bug won't allow us to use `1 - ( 0.5 || 0 )` (#12497)
				temp = remaining / animation.duration || 0,
				percent = 1 - temp,
				index = 0,
				length = animation.tweens.length;

			for ( ; index < length; index++ ) {
				animation.tweens[ index ].run( percent );
			}

			deferred.notifyWith( elem, [ animation, percent, remaining ] );

			// If there's more to do, yield
			if ( percent < 1 && length ) {
				return remaining;
			}

			// If this was an empty animation, synthesize a final progress notification
			if ( !length ) {
				deferred.notifyWith( elem, [ animation, 1, 0 ] );
			}

			// Resolve the animation and report its conclusion
			deferred.resolveWith( elem, [ animation ] );
			return false;
		},
		animation = deferred.promise( {
			elem: elem,
			props: jQuery.extend( {}, properties ),
			opts: jQuery.extend( true, {
				specialEasing: {},
				easing: jQuery.easing._default
			}, options ),
			originalProperties: properties,
			originalOptions: options,
			startTime: fxNow || createFxNow(),
			duration: options.duration,
			tweens: [],
			createTween: function( prop, end ) {
				var tween = jQuery.Tween( elem, animation.opts, prop, end,
						animation.opts.specialEasing[ prop ] || animation.opts.easing );
				animation.tweens.push( tween );
				return tween;
			},
			stop: function( gotoEnd ) {
				var index = 0,

					// If we are going to the end, we want to run all the tweens
					// otherwise we skip this part
					length = gotoEnd ? animation.tweens.length : 0;
				if ( stopped ) {
					return this;
				}
				stopped = true;
				for ( ; index < length; index++ ) {
					animation.tweens[ index ].run( 1 );
				}

				// Resolve when we played the last frame; otherwise, reject
				if ( gotoEnd ) {
					deferred.notifyWith( elem, [ animation, 1, 0 ] );
					deferred.resolveWith( elem, [ animation, gotoEnd ] );
				} else {
					deferred.rejectWith( elem, [ animation, gotoEnd ] );
				}
				return this;
			}
		} ),
		props = animation.props;

	propFilter( props, animation.opts.specialEasing );

	for ( ; index < length; index++ ) {
		result = Animation.prefilters[ index ].call( animation, elem, props, animation.opts );
		if ( result ) {
			if ( isFunction( result.stop ) ) {
				jQuery._queueHooks( animation.elem, animation.opts.queue ).stop =
					result.stop.bind( result );
			}
			return result;
		}
	}

	jQuery.map( props, createTween, animation );

	if ( isFunction( animation.opts.start ) ) {
		animation.opts.start.call( elem, animation );
	}

	// Attach callbacks from options
	animation
		.progress( animation.opts.progress )
		.done( animation.opts.done, animation.opts.complete )
		.fail( animation.opts.fail )
		.always( animation.opts.always );

	jQuery.fx.timer(
		jQuery.extend( tick, {
			elem: elem,
			anim: animation,
			queue: animation.opts.queue
		} )
	);

	return animation;
}

jQuery.Animation = jQuery.extend( Animation, {

	tweeners: {
		"*": [ function( prop, value ) {
			var tween = this.createTween( prop, value );
			adjustCSS( tween.elem, prop, rcssNum.exec( value ), tween );
			return tween;
		} ]
	},

	tweener: function( props, callback ) {
		if ( isFunction( props ) ) {
			callback = props;
			props = [ "*" ];
		} else {
			props = props.match( rnothtmlwhite );
		}

		var prop,
			index = 0,
			length = props.length;

		for ( ; index < length; index++ ) {
			prop = props[ index ];
			Animation.tweeners[ prop ] = Animation.tweeners[ prop ] || [];
			Animation.tweeners[ prop ].unshift( callback );
		}
	},

	prefilters: [ defaultPrefilter ],

	prefilter: function( callback, prepend ) {
		if ( prepend ) {
			Animation.prefilters.unshift( callback );
		} else {
			Animation.prefilters.push( callback );
		}
	}
} );

jQuery.speed = function( speed, easing, fn ) {
	var opt = speed && typeof speed === "object" ? jQuery.extend( {}, speed ) : {
		complete: fn || !fn && easing ||
			isFunction( speed ) && speed,
		duration: speed,
		easing: fn && easing || easing && !isFunction( easing ) && easing
	};

	// Go to the end state if fx are off
	if ( jQuery.fx.off ) {
		opt.duration = 0;

	} else {
		if ( typeof opt.duration !== "number" ) {
			if ( opt.duration in jQuery.fx.speeds ) {
				opt.duration = jQuery.fx.speeds[ opt.duration ];

			} else {
				opt.duration = jQuery.fx.speeds._default;
			}
		}
	}

	// Normalize opt.queue - true/undefined/null -> "fx"
	if ( opt.queue == null || opt.queue === true ) {
		opt.queue = "fx";
	}

	// Queueing
	opt.old = opt.complete;

	opt.complete = function() {
		if ( isFunction( opt.old ) ) {
			opt.old.call( this );
		}

		if ( opt.queue ) {
			jQuery.dequeue( this, opt.queue );
		}
	};

	return opt;
};

jQuery.fn.extend( {
	fadeTo: function( speed, to, easing, callback ) {

		// Show any hidden elements after setting opacity to 0
		return this.filter( isHiddenWithinTree ).css( "opacity", 0 ).show()

			// Animate to the value specified
			.end().animate( { opacity: to }, speed, easing, callback );
	},
	animate: function( prop, speed, easing, callback ) {
		var empty = jQuery.isEmptyObject( prop ),
			optall = jQuery.speed( speed, easing, callback ),
			doAnimation = function() {

				// Operate on a copy of prop so per-property easing won't be lost
				var anim = Animation( this, jQuery.extend( {}, prop ), optall );

				// Empty animations, or finishing resolves immediately
				if ( empty || dataPriv.get( this, "finish" ) ) {
					anim.stop( true );
				}
			};
			doAnimation.finish = doAnimation;

		return empty || optall.queue === false ?
			this.each( doAnimation ) :
			this.queue( optall.queue, doAnimation );
	},
	stop: function( type, clearQueue, gotoEnd ) {
		var stopQueue = function( hooks ) {
			var stop = hooks.stop;
			delete hooks.stop;
			stop( gotoEnd );
		};

		if ( typeof type !== "string" ) {
			gotoEnd = clearQueue;
			clearQueue = type;
			type = undefined;
		}
		if ( clearQueue ) {
			this.queue( type || "fx", [] );
		}

		return this.each( function() {
			var dequeue = true,
				index = type != null && type + "queueHooks",
				timers = jQuery.timers,
				data = dataPriv.get( this );

			if ( index ) {
				if ( data[ index ] && data[ index ].stop ) {
					stopQueue( data[ index ] );
				}
			} else {
				for ( index in data ) {
					if ( data[ index ] && data[ index ].stop && rrun.test( index ) ) {
						stopQueue( data[ index ] );
					}
				}
			}

			for ( index = timers.length; index--; ) {
				if ( timers[ index ].elem === this &&
					( type == null || timers[ index ].queue === type ) ) {

					timers[ index ].anim.stop( gotoEnd );
					dequeue = false;
					timers.splice( index, 1 );
				}
			}

			// Start the next in the queue if the last step wasn't forced.
			// Timers currently will call their complete callbacks, which
			// will dequeue but only if they were gotoEnd.
			if ( dequeue || !gotoEnd ) {
				jQuery.dequeue( this, type );
			}
		} );
	},
	finish: function( type ) {
		if ( type !== false ) {
			type = type || "fx";
		}
		return this.each( function() {
			var index,
				data = dataPriv.get( this ),
				queue = data[ type + "queue" ],
				hooks = data[ type + "queueHooks" ],
				timers = jQuery.timers,
				length = queue ? queue.length : 0;

			// Enable finishing flag on private data
			data.finish = true;

			// Empty the queue first
			jQuery.queue( this, type, [] );

			if ( hooks && hooks.stop ) {
				hooks.stop.call( this, true );
			}

			// Look for any active animations, and finish them
			for ( index = timers.length; index--; ) {
				if ( timers[ index ].elem === this && timers[ index ].queue === type ) {
					timers[ index ].anim.stop( true );
					timers.splice( index, 1 );
				}
			}

			// Look for any animations in the old queue and finish them
			for ( index = 0; index < length; index++ ) {
				if ( queue[ index ] && queue[ index ].finish ) {
					queue[ index ].finish.call( this );
				}
			}

			// Turn off finishing flag
			delete data.finish;
		} );
	}
} );

jQuery.each( [ "toggle", "show", "hide" ], function( _i, name ) {
	var cssFn = jQuery.fn[ name ];
	jQuery.fn[ name ] = function( speed, easing, callback ) {
		return speed == null || typeof speed === "boolean" ?
			cssFn.apply( this, arguments ) :
			this.animate( genFx( name, true ), speed, easing, callback );
	};
} );

// Generate shortcuts for custom animations
jQuery.each( {
	slideDown: genFx( "show" ),
	slideUp: genFx( "hide" ),
	slideToggle: genFx( "toggle" ),
	fadeIn: { opacity: "show" },
	fadeOut: { opacity: "hide" },
	fadeToggle: { opacity: "toggle" }
}, function( name, props ) {
	jQuery.fn[ name ] = function( speed, easing, callback ) {
		return this.animate( props, speed, easing, callback );
	};
} );

jQuery.timers = [];
jQuery.fx.tick = function() {
	var timer,
		i = 0,
		timers = jQuery.timers;

	fxNow = Date.now();

	for ( ; i < timers.length; i++ ) {
		timer = timers[ i ];

		// Run the timer and safely remove it when done (allowing for external removal)
		if ( !timer() && timers[ i ] === timer ) {
			timers.splice( i--, 1 );
		}
	}

	if ( !timers.length ) {
		jQuery.fx.stop();
	}
	fxNow = undefined;
};

jQuery.fx.timer = function( timer ) {
	jQuery.timers.push( timer );
	jQuery.fx.start();
};

jQuery.fx.interval = 13;
jQuery.fx.start = function() {
	if ( inProgress ) {
		return;
	}

	inProgress = true;
	schedule();
};

jQuery.fx.stop = function() {
	inProgress = null;
};

jQuery.fx.speeds = {
	slow: 600,
	fast: 200,

	// Default speed
	_default: 400
};


// Based off of the plugin by Clint Helfers, with permission.
// https://web.archive.org/web/20100324014747/http://blindsignals.com/index.php/2009/07/jquery-delay/
jQuery.fn.delay = function( time, type ) {
	time = jQuery.fx ? jQuery.fx.speeds[ time ] || time : time;
	type = type || "fx";

	return this.queue( type, function( next, hooks ) {
		var timeout = window.setTimeout( next, time );
		hooks.stop = function() {
			window.clearTimeout( timeout );
		};
	} );
};


( function() {
	var input = document.createElement( "input" ),
		select = document.createElement( "select" ),
		opt = select.appendChild( document.createElement( "option" ) );

	input.type = "checkbox";

	// Support: Android <=4.3 only
	// Default value for a checkbox should be "on"
	support.checkOn = input.value !== "";

	// Support: IE <=11 only
	// Must access selectedIndex to make default options select
	support.optSelected = opt.selected;

	// Support: IE <=11 only
	// An input loses its value after becoming a radio
	input = document.createElement( "input" );
	input.value = "t";
	input.type = "radio";
	support.radioValue = input.value === "t";
} )();


var boolHook,
	attrHandle = jQuery.expr.attrHandle;

jQuery.fn.extend( {
	attr: function( name, value ) {
		return access( this, jQuery.attr, name, value, arguments.length > 1 );
	},

	removeAttr: function( name ) {
		return this.each( function() {
			jQuery.removeAttr( this, name );
		} );
	}
} );

jQuery.extend( {
	attr: function( elem, name, value ) {
		var ret, hooks,
			nType = elem.nodeType;

		// Don't get/set attributes on text, comment and attribute nodes
		if ( nType === 3 || nType === 8 || nType === 2 ) {
			return;
		}

		// Fallback to prop when attributes are not supported
		if ( typeof elem.getAttribute === "undefined" ) {
			return jQuery.prop( elem, name, value );
		}

		// Attribute hooks are determined by the lowercase version
		// Grab necessary hook if one is defined
		if ( nType !== 1 || !jQuery.isXMLDoc( elem ) ) {
			hooks = jQuery.attrHooks[ name.toLowerCase() ] ||
				( jQuery.expr.match.bool.test( name ) ? boolHook : undefined );
		}

		if ( value !== undefined ) {
			if ( value === null ) {
				jQuery.removeAttr( elem, name );
				return;
			}

			if ( hooks && "set" in hooks &&
				( ret = hooks.set( elem, value, name ) ) !== undefined ) {
				return ret;
			}

			elem.setAttribute( name, value + "" );
			return value;
		}

		if ( hooks && "get" in hooks && ( ret = hooks.get( elem, name ) ) !== null ) {
			return ret;
		}

		ret = jQuery.find.attr( elem, name );

		// Non-existent attributes return null, we normalize to undefined
		return ret == null ? undefined : ret;
	},

	attrHooks: {
		type: {
			set: function( elem, value ) {
				if ( !support.radioValue && value === "radio" &&
					nodeName( elem, "input" ) ) {
					var val = elem.value;
					elem.setAttribute( "type", value );
					if ( val ) {
						elem.value = val;
					}
					return value;
				}
			}
		}
	},

	removeAttr: function( elem, value ) {
		var name,
			i = 0,

			// Attribute names can contain non-HTML whitespace characters
			// https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
			attrNames = value && value.match( rnothtmlwhite );

		if ( attrNames && elem.nodeType === 1 ) {
			while ( ( name = attrNames[ i++ ] ) ) {
				elem.removeAttribute( name );
			}
		}
	}
} );

// Hooks for boolean attributes
boolHook = {
	set: function( elem, value, name ) {
		if ( value === false ) {

			// Remove boolean attributes when set to false
			jQuery.removeAttr( elem, name );
		} else {
			elem.setAttribute( name, name );
		}
		return name;
	}
};

jQuery.each( jQuery.expr.match.bool.source.match( /\w+/g ), function( _i, name ) {
	var getter = attrHandle[ name ] || jQuery.find.attr;

	attrHandle[ name ] = function( elem, name, isXML ) {
		var ret, handle,
			lowercaseName = name.toLowerCase();

		if ( !isXML ) {

			// Avoid an infinite loop by temporarily removing this function from the getter
			handle = attrHandle[ lowercaseName ];
			attrHandle[ lowercaseName ] = ret;
			ret = getter( elem, name, isXML ) != null ?
				lowercaseName :
				null;
			attrHandle[ lowercaseName ] = handle;
		}
		return ret;
	};
} );




var rfocusable = /^(?:input|select|textarea|button)$/i,
	rclickable = /^(?:a|area)$/i;

jQuery.fn.extend( {
	prop: function( name, value ) {
		return access( this, jQuery.prop, name, value, arguments.length > 1 );
	},

	removeProp: function( name ) {
		return this.each( function() {
			delete this[ jQuery.propFix[ name ] || name ];
		} );
	}
} );

jQuery.extend( {
	prop: function( elem, name, value ) {
		var ret, hooks,
			nType = elem.nodeType;

		// Don't get/set properties on text, comment and attribute nodes
		if ( nType === 3 || nType === 8 || nType === 2 ) {
			return;
		}

		if ( nType !== 1 || !jQuery.isXMLDoc( elem ) ) {

			// Fix name and attach hooks
			name = jQuery.propFix[ name ] || name;
			hooks = jQuery.propHooks[ name ];
		}

		if ( value !== undefined ) {
			if ( hooks && "set" in hooks &&
				( ret = hooks.set( elem, value, name ) ) !== undefined ) {
				return ret;
			}

			return ( elem[ name ] = value );
		}

		if ( hooks && "get" in hooks && ( ret = hooks.get( elem, name ) ) !== null ) {
			return ret;
		}

		return elem[ name ];
	},

	propHooks: {
		tabIndex: {
			get: function( elem ) {

				// Support: IE <=9 - 11 only
				// elem.tabIndex doesn't always return the
				// correct value when it hasn't been explicitly set
				// https://web.archive.org/web/20141116233347/http://fluidproject.org/blog/2008/01/09/getting-setting-and-removing-tabindex-values-with-javascript/
				// Use proper attribute retrieval(#12072)
				var tabindex = jQuery.find.attr( elem, "tabindex" );

				if ( tabindex ) {
					return parseInt( tabindex, 10 );
				}

				if (
					rfocusable.test( elem.nodeName ) ||
					rclickable.test( elem.nodeName ) &&
					elem.href
				) {
					return 0;
				}

				return -1;
			}
		}
	},

	propFix: {
		"for": "htmlFor",
		"class": "className"
	}
} );

// Support: IE <=11 only
// Accessing the selectedIndex property
// forces the browser to respect setting selected
// on the option
// The getter ensures a default option is selected
// when in an optgroup
// eslint rule "no-unused-expressions" is disabled for this code
// since it considers such accessions noop
if ( !support.optSelected ) {
	jQuery.propHooks.selected = {
		get: function( elem ) {

			/* eslint no-unused-expressions: "off" */

			var parent = elem.parentNode;
			if ( parent && parent.parentNode ) {
				parent.parentNode.selectedIndex;
			}
			return null;
		},
		set: function( elem ) {

			/* eslint no-unused-expressions: "off" */

			var parent = elem.parentNode;
			if ( parent ) {
				parent.selectedIndex;

				if ( parent.parentNode ) {
					parent.parentNode.selectedIndex;
				}
			}
		}
	};
}

jQuery.each( [
	"tabIndex",
	"readOnly",
	"maxLength",
	"cellSpacing",
	"cellPadding",
	"rowSpan",
	"colSpan",
	"useMap",
	"frameBorder",
	"contentEditable"
], function() {
	jQuery.propFix[ this.toLowerCase() ] = this;
} );




	// Strip and collapse whitespace according to HTML spec
	// https://infra.spec.whatwg.org/#strip-and-collapse-ascii-whitespace
	function stripAndCollapse( value ) {
		var tokens = value.match( rnothtmlwhite ) || [];
		return tokens.join( " " );
	}


function getClass( elem ) {
	return elem.getAttribute && elem.getAttribute( "class" ) || "";
}

function classesToArray( value ) {
	if ( Array.isArray( value ) ) {
		return value;
	}
	if ( typeof value === "string" ) {
		return value.match( rnothtmlwhite ) || [];
	}
	return [];
}

jQuery.fn.extend( {
	addClass: function( value ) {
		var classes, elem, cur, curValue, clazz, j, finalValue,
			i = 0;

		if ( isFunction( value ) ) {
			return this.each( function( j ) {
				jQuery( this ).addClass( value.call( this, j, getClass( this ) ) );
			} );
		}

		classes = classesToArray( value );

		if ( classes.length ) {
			while ( ( elem = this[ i++ ] ) ) {
				curValue = getClass( elem );
				cur = elem.nodeType === 1 && ( " " + stripAndCollapse( curValue ) + " " );

				if ( cur ) {
					j = 0;
					while ( ( clazz = classes[ j++ ] ) ) {
						if ( cur.indexOf( " " + clazz + " " ) < 0 ) {
							cur += clazz + " ";
						}
					}

					// Only assign if different to avoid unneeded rendering.
					finalValue = stripAndCollapse( cur );
					if ( curValue !== finalValue ) {
						elem.setAttribute( "class", finalValue );
					}
				}
			}
		}

		return this;
	},

	removeClass: function( value ) {
		var classes, elem, cur, curValue, clazz, j, finalValue,
			i = 0;

		if ( isFunction( value ) ) {
			return this.each( function( j ) {
				jQuery( this ).removeClass( value.call( this, j, getClass( this ) ) );
			} );
		}

		if ( !arguments.length ) {
			return this.attr( "class", "" );
		}

		classes = classesToArray( value );

		if ( classes.length ) {
			while ( ( elem = this[ i++ ] ) ) {
				curValue = getClass( elem );

				// This expression is here for better compressibility (see addClass)
				cur = elem.nodeType === 1 && ( " " + stripAndCollapse( curValue ) + " " );

				if ( cur ) {
					j = 0;
					while ( ( clazz = classes[ j++ ] ) ) {

						// Remove *all* instances
						while ( cur.indexOf( " " + clazz + " " ) > -1 ) {
							cur = cur.replace( " " + clazz + " ", " " );
						}
					}

					// Only assign if different to avoid unneeded rendering.
					finalValue = stripAndCollapse( cur );
					if ( curValue !== finalValue ) {
						elem.setAttribute( "class", finalValue );
					}
				}
			}
		}

		return this;
	},

	toggleClass: function( value, stateVal ) {
		var type = typeof value,
			isValidValue = type === "string" || Array.isArray( value );

		if ( typeof stateVal === "boolean" && isValidValue ) {
			return stateVal ? this.addClass( value ) : this.removeClass( value );
		}

		if ( isFunction( value ) ) {
			return this.each( function( i ) {
				jQuery( this ).toggleClass(
					value.call( this, i, getClass( this ), stateVal ),
					stateVal
				);
			} );
		}

		return this.each( function() {
			var className, i, self, classNames;

			if ( isValidValue ) {

				// Toggle individual class names
				i = 0;
				self = jQuery( this );
				classNames = classesToArray( value );

				while ( ( className = classNames[ i++ ] ) ) {

					// Check each className given, space separated list
					if ( self.hasClass( className ) ) {
						self.removeClass( className );
					} else {
						self.addClass( className );
					}
				}

			// Toggle whole class name
			} else if ( value === undefined || type === "boolean" ) {
				className = getClass( this );
				if ( className ) {

					// Store className if set
					dataPriv.set( this, "__className__", className );
				}

				// If the element has a class name or if we're passed `false`,
				// then remove the whole classname (if there was one, the above saved it).
				// Otherwise bring back whatever was previously saved (if anything),
				// falling back to the empty string if nothing was stored.
				if ( this.setAttribute ) {
					this.setAttribute( "class",
						className || value === false ?
						"" :
						dataPriv.get( this, "__className__" ) || ""
					);
				}
			}
		} );
	},

	hasClass: function( selector ) {
		var className, elem,
			i = 0;

		className = " " + selector + " ";
		while ( ( elem = this[ i++ ] ) ) {
			if ( elem.nodeType === 1 &&
				( " " + stripAndCollapse( getClass( elem ) ) + " " ).indexOf( className ) > -1 ) {
					return true;
			}
		}

		return false;
	}
} );




var rreturn = /\r/g;

jQuery.fn.extend( {
	val: function( value ) {
		var hooks, ret, valueIsFunction,
			elem = this[ 0 ];

		if ( !arguments.length ) {
			if ( elem ) {
				hooks = jQuery.valHooks[ elem.type ] ||
					jQuery.valHooks[ elem.nodeName.toLowerCase() ];

				if ( hooks &&
					"get" in hooks &&
					( ret = hooks.get( elem, "value" ) ) !== undefined
				) {
					return ret;
				}

				ret = elem.value;

				// Handle most common string cases
				if ( typeof ret === "string" ) {
					return ret.replace( rreturn, "" );
				}

				// Handle cases where value is null/undef or number
				return ret == null ? "" : ret;
			}

			return;
		}

		valueIsFunction = isFunction( value );

		return this.each( function( i ) {
			var val;

			if ( this.nodeType !== 1 ) {
				return;
			}

			if ( valueIsFunction ) {
				val = value.call( this, i, jQuery( this ).val() );
			} else {
				val = value;
			}

			// Treat null/undefined as ""; convert numbers to string
			if ( val == null ) {
				val = "";

			} else if ( typeof val === "number" ) {
				val += "";

			} else if ( Array.isArray( val ) ) {
				val = jQuery.map( val, function( value ) {
					return value == null ? "" : value + "";
				} );
			}

			hooks = jQuery.valHooks[ this.type ] || jQuery.valHooks[ this.nodeName.toLowerCase() ];

			// If set returns undefined, fall back to normal setting
			if ( !hooks || !( "set" in hooks ) || hooks.set( this, val, "value" ) === undefined ) {
				this.value = val;
			}
		} );
	}
} );

jQuery.extend( {
	valHooks: {
		option: {
			get: function( elem ) {

				var val = jQuery.find.attr( elem, "value" );
				return val != null ?
					val :

					// Support: IE <=10 - 11 only
					// option.text throws exceptions (#14686, #14858)
					// Strip and collapse whitespace
					// https://html.spec.whatwg.org/#strip-and-collapse-whitespace
					stripAndCollapse( jQuery.text( elem ) );
			}
		},
		select: {
			get: function( elem ) {
				var value, option, i,
					options = elem.options,
					index = elem.selectedIndex,
					one = elem.type === "select-one",
					values = one ? null : [],
					max = one ? index + 1 : options.length;

				if ( index < 0 ) {
					i = max;

				} else {
					i = one ? index : 0;
				}

				// Loop through all the selected options
				for ( ; i < max; i++ ) {
					option = options[ i ];

					// Support: IE <=9 only
					// IE8-9 doesn't update selected after form reset (#2551)
					if ( ( option.selected || i === index ) &&

							// Don't return options that are disabled or in a disabled optgroup
							!option.disabled &&
							( !option.parentNode.disabled ||
								!nodeName( option.parentNode, "optgroup" ) ) ) {

						// Get the specific value for the option
						value = jQuery( option ).val();

						// We don't need an array for one selects
						if ( one ) {
							return value;
						}

						// Multi-Selects return an array
						values.push( value );
					}
				}

				return values;
			},

			set: function( elem, value ) {
				var optionSet, option,
					options = elem.options,
					values = jQuery.makeArray( value ),
					i = options.length;

				while ( i-- ) {
					option = options[ i ];

					/* eslint-disable no-cond-assign */

					if ( option.selected =
						jQuery.inArray( jQuery.valHooks.option.get( option ), values ) > -1
					) {
						optionSet = true;
					}

					/* eslint-enable no-cond-assign */
				}

				// Force browsers to behave consistently when non-matching value is set
				if ( !optionSet ) {
					elem.selectedIndex = -1;
				}
				return values;
			}
		}
	}
} );

// Radios and checkboxes getter/setter
jQuery.each( [ "radio", "checkbox" ], function() {
	jQuery.valHooks[ this ] = {
		set: function( elem, value ) {
			if ( Array.isArray( value ) ) {
				return ( elem.checked = jQuery.inArray( jQuery( elem ).val(), value ) > -1 );
			}
		}
	};
	if ( !support.checkOn ) {
		jQuery.valHooks[ this ].get = function( elem ) {
			return elem.getAttribute( "value" ) === null ? "on" : elem.value;
		};
	}
} );




// Return jQuery for attributes-only inclusion


support.focusin = "onfocusin" in window;


var rfocusMorph = /^(?:focusinfocus|focusoutblur)$/,
	stopPropagationCallback = function( e ) {
		e.stopPropagation();
	};

jQuery.extend( jQuery.event, {

	trigger: function( event, data, elem, onlyHandlers ) {

		var i, cur, tmp, bubbleType, ontype, handle, special, lastElement,
			eventPath = [ elem || document ],
			type = hasOwn.call( event, "type" ) ? event.type : event,
			namespaces = hasOwn.call( event, "namespace" ) ? event.namespace.split( "." ) : [];

		cur = lastElement = tmp = elem = elem || document;

		// Don't do events on text and comment nodes
		if ( elem.nodeType === 3 || elem.nodeType === 8 ) {
			return;
		}

		// focus/blur morphs to focusin/out; ensure we're not firing them right now
		if ( rfocusMorph.test( type + jQuery.event.triggered ) ) {
			return;
		}

		if ( type.indexOf( "." ) > -1 ) {

			// Namespaced trigger; create a regexp to match event type in handle()
			namespaces = type.split( "." );
			type = namespaces.shift();
			namespaces.sort();
		}
		ontype = type.indexOf( ":" ) < 0 && "on" + type;

		// Caller can pass in a jQuery.Event object, Object, or just an event type string
		event = event[ jQuery.expando ] ?
			event :
			new jQuery.Event( type, typeof event === "object" && event );

		// Trigger bitmask: & 1 for native handlers; & 2 for jQuery (always true)
		event.isTrigger = onlyHandlers ? 2 : 3;
		event.namespace = namespaces.join( "." );
		event.rnamespace = event.namespace ?
			new RegExp( "(^|\\.)" + namespaces.join( "\\.(?:.*\\.|)" ) + "(\\.|$)" ) :
			null;

		// Clean up the event in case it is being reused
		event.result = undefined;
		if ( !event.target ) {
			event.target = elem;
		}

		// Clone any incoming data and prepend the event, creating the handler arg list
		data = data == null ?
			[ event ] :
			jQuery.makeArray( data, [ event ] );

		// Allow special events to draw outside the lines
		special = jQuery.event.special[ type ] || {};
		if ( !onlyHandlers && special.trigger && special.trigger.apply( elem, data ) === false ) {
			return;
		}

		// Determine event propagation path in advance, per W3C events spec (#9951)
		// Bubble up to document, then to window; watch for a global ownerDocument var (#9724)
		if ( !onlyHandlers && !special.noBubble && !isWindow( elem ) ) {

			bubbleType = special.delegateType || type;
			if ( !rfocusMorph.test( bubbleType + type ) ) {
				cur = cur.parentNode;
			}
			for ( ; cur; cur = cur.parentNode ) {
				eventPath.push( cur );
				tmp = cur;
			}

			// Only add window if we got to document (e.g., not plain obj or detached DOM)
			if ( tmp === ( elem.ownerDocument || document ) ) {
				eventPath.push( tmp.defaultView || tmp.parentWindow || window );
			}
		}

		// Fire handlers on the event path
		i = 0;
		while ( ( cur = eventPath[ i++ ] ) && !event.isPropagationStopped() ) {
			lastElement = cur;
			event.type = i > 1 ?
				bubbleType :
				special.bindType || type;

			// jQuery handler
			handle = (
					dataPriv.get( cur, "events" ) || Object.create( null )
				)[ event.type ] &&
				dataPriv.get( cur, "handle" );
			if ( handle ) {
				handle.apply( cur, data );
			}

			// Native handler
			handle = ontype && cur[ ontype ];
			if ( handle && handle.apply && acceptData( cur ) ) {
				event.result = handle.apply( cur, data );
				if ( event.result === false ) {
					event.preventDefault();
				}
			}
		}
		event.type = type;

		// If nobody prevented the default action, do it now
		if ( !onlyHandlers && !event.isDefaultPrevented() ) {

			if ( ( !special._default ||
				special._default.apply( eventPath.pop(), data ) === false ) &&
				acceptData( elem ) ) {

				// Call a native DOM method on the target with the same name as the event.
				// Don't do default actions on window, that's where global variables be (#6170)
				if ( ontype && isFunction( elem[ type ] ) && !isWindow( elem ) ) {

					// Don't re-trigger an onFOO event when we call its FOO() method
					tmp = elem[ ontype ];

					if ( tmp ) {
						elem[ ontype ] = null;
					}

					// Prevent re-triggering of the same event, since we already bubbled it above
					jQuery.event.triggered = type;

					if ( event.isPropagationStopped() ) {
						lastElement.addEventListener( type, stopPropagationCallback );
					}

					elem[ type ]();

					if ( event.isPropagationStopped() ) {
						lastElement.removeEventListener( type, stopPropagationCallback );
					}

					jQuery.event.triggered = undefined;

					if ( tmp ) {
						elem[ ontype ] = tmp;
					}
				}
			}
		}

		return event.result;
	},

	// Piggyback on a donor event to simulate a different one
	// Used only for `focus(in | out)` events
	simulate: function( type, elem, event ) {
		var e = jQuery.extend(
			new jQuery.Event(),
			event,
			{
				type: type,
				isSimulated: true
			}
		);

		jQuery.event.trigger( e, null, elem );
	}

} );

jQuery.fn.extend( {

	trigger: function( type, data ) {
		return this.each( function() {
			jQuery.event.trigger( type, data, this );
		} );
	},
	triggerHandler: function( type, data ) {
		var elem = this[ 0 ];
		if ( elem ) {
			return jQuery.event.trigger( type, data, elem, true );
		}
	}
} );


// Support: Firefox <=44
// Firefox doesn't have focus(in | out) events
// Related ticket - https://bugzilla.mozilla.org/show_bug.cgi?id=687787
//
// Support: Chrome <=48 - 49, Safari <=9.0 - 9.1
// focus(in | out) events fire after focus & blur events,
// which is spec violation - http://www.w3.org/TR/DOM-Level-3-Events/#events-focusevent-event-order
// Related ticket - https://bugs.chromium.org/p/chromium/issues/detail?id=449857
if ( !support.focusin ) {
	jQuery.each( { focus: "focusin", blur: "focusout" }, function( orig, fix ) {

		// Attach a single capturing handler on the document while someone wants focusin/focusout
		var handler = function( event ) {
			jQuery.event.simulate( fix, event.target, jQuery.event.fix( event ) );
		};

		jQuery.event.special[ fix ] = {
			setup: function() {

				// Handle: regular nodes (via `this.ownerDocument`), window
				// (via `this.document`) & document (via `this`).
				var doc = this.ownerDocument || this.document || this,
					attaches = dataPriv.access( doc, fix );

				if ( !attaches ) {
					doc.addEventListener( orig, handler, true );
				}
				dataPriv.access( doc, fix, ( attaches || 0 ) + 1 );
			},
			teardown: function() {
				var doc = this.ownerDocument || this.document || this,
					attaches = dataPriv.access( doc, fix ) - 1;

				if ( !attaches ) {
					doc.removeEventListener( orig, handler, true );
					dataPriv.remove( doc, fix );

				} else {
					dataPriv.access( doc, fix, attaches );
				}
			}
		};
	} );
}
var location = window.location;

var nonce = { guid: Date.now() };

var rquery = ( /\?/ );



// Cross-browser xml parsing
jQuery.parseXML = function( data ) {
	var xml;
	if ( !data || typeof data !== "string" ) {
		return null;
	}

	// Support: IE 9 - 11 only
	// IE throws on parseFromString with invalid input.
	try {
		xml = ( new window.DOMParser() ).parseFromString( data, "text/xml" );
	} catch ( e ) {
		xml = undefined;
	}

	if ( !xml || xml.getElementsByTagName( "parsererror" ).length ) {
		jQuery.error( "Invalid XML: " + data );
	}
	return xml;
};


var
	rbracket = /\[\]$/,
	rCRLF = /\r?\n/g,
	rsubmitterTypes = /^(?:submit|button|image|reset|file)$/i,
	rsubmittable = /^(?:input|select|textarea|keygen)/i;

function buildParams( prefix, obj, traditional, add ) {
	var name;

	if ( Array.isArray( obj ) ) {

		// Serialize array item.
		jQuery.each( obj, function( i, v ) {
			if ( traditional || rbracket.test( prefix ) ) {

				// Treat each array item as a scalar.
				add( prefix, v );

			} else {

				// Item is non-scalar (array or object), encode its numeric index.
				buildParams(
					prefix + "[" + ( typeof v === "object" && v != null ? i : "" ) + "]",
					v,
					traditional,
					add
				);
			}
		} );

	} else if ( !traditional && toType( obj ) === "object" ) {

		// Serialize object item.
		for ( name in obj ) {
			buildParams( prefix + "[" + name + "]", obj[ name ], traditional, add );
		}

	} else {

		// Serialize scalar item.
		add( prefix, obj );
	}
}

// Serialize an array of form elements or a set of
// key/values into a query string
jQuery.param = function( a, traditional ) {
	var prefix,
		s = [],
		add = function( key, valueOrFunction ) {

			// If value is a function, invoke it and use its return value
			var value = isFunction( valueOrFunction ) ?
				valueOrFunction() :
				valueOrFunction;

			s[ s.length ] = encodeURIComponent( key ) + "=" +
				encodeURIComponent( value == null ? "" : value );
		};

	if ( a == null ) {
		return "";
	}

	// If an array was passed in, assume that it is an array of form elements.
	if ( Array.isArray( a ) || ( a.jquery && !jQuery.isPlainObject( a ) ) ) {

		// Serialize the form elements
		jQuery.each( a, function() {
			add( this.name, this.value );
		} );

	} else {

		// If traditional, encode the "old" way (the way 1.3.2 or older
		// did it), otherwise encode params recursively.
		for ( prefix in a ) {
			buildParams( prefix, a[ prefix ], traditional, add );
		}
	}

	// Return the resulting serialization
	return s.join( "&" );
};

jQuery.fn.extend( {
	serialize: function() {
		return jQuery.param( this.serializeArray() );
	},
	serializeArray: function() {
		return this.map( function() {

			// Can add propHook for "elements" to filter or add form elements
			var elements = jQuery.prop( this, "elements" );
			return elements ? jQuery.makeArray( elements ) : this;
		} )
		.filter( function() {
			var type = this.type;

			// Use .is( ":disabled" ) so that fieldset[disabled] works
			return this.name && !jQuery( this ).is( ":disabled" ) &&
				rsubmittable.test( this.nodeName ) && !rsubmitterTypes.test( type ) &&
				( this.checked || !rcheckableType.test( type ) );
		} )
		.map( function( _i, elem ) {
			var val = jQuery( this ).val();

			if ( val == null ) {
				return null;
			}

			if ( Array.isArray( val ) ) {
				return jQuery.map( val, function( val ) {
					return { name: elem.name, value: val.replace( rCRLF, "\r\n" ) };
				} );
			}

			return { name: elem.name, value: val.replace( rCRLF, "\r\n" ) };
		} ).get();
	}
} );


var
	r20 = /%20/g,
	rhash = /#.*$/,
	rantiCache = /([?&])_=[^&]*/,
	rheaders = /^(.*?):[ \t]*([^\r\n]*)$/mg,

	// #7653, #8125, #8152: local protocol detection
	rlocalProtocol = /^(?:about|app|app-storage|.+-extension|file|res|widget):$/,
	rnoContent = /^(?:GET|HEAD)$/,
	rprotocol = /^\/\//,

	/* Prefilters
	 * 1) They are useful to introduce custom dataTypes (see ajax/jsonp.js for an example)
	 * 2) These are called:
	 *    - BEFORE asking for a transport
	 *    - AFTER param serialization (s.data is a string if s.processData is true)
	 * 3) key is the dataType
	 * 4) the catchall symbol "*" can be used
	 * 5) execution will start with transport dataType and THEN continue down to "*" if needed
	 */
	prefilters = {},

	/* Transports bindings
	 * 1) key is the dataType
	 * 2) the catchall symbol "*" can be used
	 * 3) selection will start with transport dataType and THEN go to "*" if needed
	 */
	transports = {},

	// Avoid comment-prolog char sequence (#10098); must appease lint and evade compression
	allTypes = "*/".concat( "*" ),

	// Anchor tag for parsing the document origin
	originAnchor = document.createElement( "a" );
	originAnchor.href = location.href;

// Base "constructor" for jQuery.ajaxPrefilter and jQuery.ajaxTransport
function addToPrefiltersOrTransports( structure ) {

	// dataTypeExpression is optional and defaults to "*"
	return function( dataTypeExpression, func ) {

		if ( typeof dataTypeExpression !== "string" ) {
			func = dataTypeExpression;
			dataTypeExpression = "*";
		}

		var dataType,
			i = 0,
			dataTypes = dataTypeExpression.toLowerCase().match( rnothtmlwhite ) || [];

		if ( isFunction( func ) ) {

			// For each dataType in the dataTypeExpression
			while ( ( dataType = dataTypes[ i++ ] ) ) {

				// Prepend if requested
				if ( dataType[ 0 ] === "+" ) {
					dataType = dataType.slice( 1 ) || "*";
					( structure[ dataType ] = structure[ dataType ] || [] ).unshift( func );

				// Otherwise append
				} else {
					( structure[ dataType ] = structure[ dataType ] || [] ).push( func );
				}
			}
		}
	};
}

// Base inspection function for prefilters and transports
function inspectPrefiltersOrTransports( structure, options, originalOptions, jqXHR ) {

	var inspected = {},
		seekingTransport = ( structure === transports );

	function inspect( dataType ) {
		var selected;
		inspected[ dataType ] = true;
		jQuery.each( structure[ dataType ] || [], function( _, prefilterOrFactory ) {
			var dataTypeOrTransport = prefilterOrFactory( options, originalOptions, jqXHR );
			if ( typeof dataTypeOrTransport === "string" &&
				!seekingTransport && !inspected[ dataTypeOrTransport ] ) {

				options.dataTypes.unshift( dataTypeOrTransport );
				inspect( dataTypeOrTransport );
				return false;
			} else if ( seekingTransport ) {
				return !( selected = dataTypeOrTransport );
			}
		} );
		return selected;
	}

	return inspect( options.dataTypes[ 0 ] ) || !inspected[ "*" ] && inspect( "*" );
}

// A special extend for ajax options
// that takes "flat" options (not to be deep extended)
// Fixes #9887
function ajaxExtend( target, src ) {
	var key, deep,
		flatOptions = jQuery.ajaxSettings.flatOptions || {};

	for ( key in src ) {
		if ( src[ key ] !== undefined ) {
			( flatOptions[ key ] ? target : ( deep || ( deep = {} ) ) )[ key ] = src[ key ];
		}
	}
	if ( deep ) {
		jQuery.extend( true, target, deep );
	}

	return target;
}

/* Handles responses to an ajax request:
 * - finds the right dataType (mediates between content-type and expected dataType)
 * - returns the corresponding response
 */
function ajaxHandleResponses( s, jqXHR, responses ) {

	var ct, type, finalDataType, firstDataType,
		contents = s.contents,
		dataTypes = s.dataTypes;

	// Remove auto dataType and get content-type in the process
	while ( dataTypes[ 0 ] === "*" ) {
		dataTypes.shift();
		if ( ct === undefined ) {
			ct = s.mimeType || jqXHR.getResponseHeader( "Content-Type" );
		}
	}

	// Check if we're dealing with a known content-type
	if ( ct ) {
		for ( type in contents ) {
			if ( contents[ type ] && contents[ type ].test( ct ) ) {
				dataTypes.unshift( type );
				break;
			}
		}
	}

	// Check to see if we have a response for the expected dataType
	if ( dataTypes[ 0 ] in responses ) {
		finalDataType = dataTypes[ 0 ];
	} else {

		// Try convertible dataTypes
		for ( type in responses ) {
			if ( !dataTypes[ 0 ] || s.converters[ type + " " + dataTypes[ 0 ] ] ) {
				finalDataType = type;
				break;
			}
			if ( !firstDataType ) {
				firstDataType = type;
			}
		}

		// Or just use first one
		finalDataType = finalDataType || firstDataType;
	}

	// If we found a dataType
	// We add the dataType to the list if needed
	// and return the corresponding response
	if ( finalDataType ) {
		if ( finalDataType !== dataTypes[ 0 ] ) {
			dataTypes.unshift( finalDataType );
		}
		return responses[ finalDataType ];
	}
}

/* Chain conversions given the request and the original response
 * Also sets the responseXXX fields on the jqXHR instance
 */
function ajaxConvert( s, response, jqXHR, isSuccess ) {
	var conv2, current, conv, tmp, prev,
		converters = {},

		// Work with a copy of dataTypes in case we need to modify it for conversion
		dataTypes = s.dataTypes.slice();

	// Create converters map with lowercased keys
	if ( dataTypes[ 1 ] ) {
		for ( conv in s.converters ) {
			converters[ conv.toLowerCase() ] = s.converters[ conv ];
		}
	}

	current = dataTypes.shift();

	// Convert to each sequential dataType
	while ( current ) {

		if ( s.responseFields[ current ] ) {
			jqXHR[ s.responseFields[ current ] ] = response;
		}

		// Apply the dataFilter if provided
		if ( !prev && isSuccess && s.dataFilter ) {
			response = s.dataFilter( response, s.dataType );
		}

		prev = current;
		current = dataTypes.shift();

		if ( current ) {

			// There's only work to do if current dataType is non-auto
			if ( current === "*" ) {

				current = prev;

			// Convert response if prev dataType is non-auto and differs from current
			} else if ( prev !== "*" && prev !== current ) {

				// Seek a direct converter
				conv = converters[ prev + " " + current ] || converters[ "* " + current ];

				// If none found, seek a pair
				if ( !conv ) {
					for ( conv2 in converters ) {

						// If conv2 outputs current
						tmp = conv2.split( " " );
						if ( tmp[ 1 ] === current ) {

							// If prev can be converted to accepted input
							conv = converters[ prev + " " + tmp[ 0 ] ] ||
								converters[ "* " + tmp[ 0 ] ];
							if ( conv ) {

								// Condense equivalence converters
								if ( conv === true ) {
									conv = converters[ conv2 ];

								// Otherwise, insert the intermediate dataType
								} else if ( converters[ conv2 ] !== true ) {
									current = tmp[ 0 ];
									dataTypes.unshift( tmp[ 1 ] );
								}
								break;
							}
						}
					}
				}

				// Apply converter (if not an equivalence)
				if ( conv !== true ) {

					// Unless errors are allowed to bubble, catch and return them
					if ( conv && s.throws ) {
						response = conv( response );
					} else {
						try {
							response = conv( response );
						} catch ( e ) {
							return {
								state: "parsererror",
								error: conv ? e : "No conversion from " + prev + " to " + current
							};
						}
					}
				}
			}
		}
	}

	return { state: "success", data: response };
}

jQuery.extend( {

	// Counter for holding the number of active queries
	active: 0,

	// Last-Modified header cache for next request
	lastModified: {},
	etag: {},

	ajaxSettings: {
		url: location.href,
		type: "GET",
		isLocal: rlocalProtocol.test( location.protocol ),
		global: true,
		processData: true,
		async: true,
		contentType: "application/x-www-form-urlencoded; charset=UTF-8",

		/*
		timeout: 0,
		data: null,
		dataType: null,
		username: null,
		password: null,
		cache: null,
		throws: false,
		traditional: false,
		headers: {},
		*/

		accepts: {
			"*": allTypes,
			text: "text/plain",
			html: "text/html",
			xml: "application/xml, text/xml",
			json: "application/json, text/javascript"
		},

		contents: {
			xml: /\bxml\b/,
			html: /\bhtml/,
			json: /\bjson\b/
		},

		responseFields: {
			xml: "responseXML",
			text: "responseText",
			json: "responseJSON"
		},

		// Data converters
		// Keys separate source (or catchall "*") and destination types with a single space
		converters: {

			// Convert anything to text
			"* text": String,

			// Text to html (true = no transformation)
			"text html": true,

			// Evaluate text as a json expression
			"text json": JSON.parse,

			// Parse text as xml
			"text xml": jQuery.parseXML
		},

		// For options that shouldn't be deep extended:
		// you can add your own custom options here if
		// and when you create one that shouldn't be
		// deep extended (see ajaxExtend)
		flatOptions: {
			url: true,
			context: true
		}
	},

	// Creates a full fledged settings object into target
	// with both ajaxSettings and settings fields.
	// If target is omitted, writes into ajaxSettings.
	ajaxSetup: function( target, settings ) {
		return settings ?

			// Building a settings object
			ajaxExtend( ajaxExtend( target, jQuery.ajaxSettings ), settings ) :

			// Extending ajaxSettings
			ajaxExtend( jQuery.ajaxSettings, target );
	},

	ajaxPrefilter: addToPrefiltersOrTransports( prefilters ),
	ajaxTransport: addToPrefiltersOrTransports( transports ),

	// Main method
	ajax: function( url, options ) {

		// If url is an object, simulate pre-1.5 signature
		if ( typeof url === "object" ) {
			options = url;
			url = undefined;
		}

		// Force options to be an object
		options = options || {};

		var transport,

			// URL without anti-cache param
			cacheURL,

			// Response headers
			responseHeadersString,
			responseHeaders,

			// timeout handle
			timeoutTimer,

			// Url cleanup var
			urlAnchor,

			// Request state (becomes false upon send and true upon completion)
			completed,

			// To know if global events are to be dispatched
			fireGlobals,

			// Loop variable
			i,

			// uncached part of the url
			uncached,

			// Create the final options object
			s = jQuery.ajaxSetup( {}, options ),

			// Callbacks context
			callbackContext = s.context || s,

			// Context for global events is callbackContext if it is a DOM node or jQuery collection
			globalEventContext = s.context &&
				( callbackContext.nodeType || callbackContext.jquery ) ?
					jQuery( callbackContext ) :
					jQuery.event,

			// Deferreds
			deferred = jQuery.Deferred(),
			completeDeferred = jQuery.Callbacks( "once memory" ),

			// Status-dependent callbacks
			statusCode = s.statusCode || {},

			// Headers (they are sent all at once)
			requestHeaders = {},
			requestHeadersNames = {},

			// Default abort message
			strAbort = "canceled",

			// Fake xhr
			jqXHR = {
				readyState: 0,

				// Builds headers hashtable if needed
				getResponseHeader: function( key ) {
					var match;
					if ( completed ) {
						if ( !responseHeaders ) {
							responseHeaders = {};
							while ( ( match = rheaders.exec( responseHeadersString ) ) ) {
								responseHeaders[ match[ 1 ].toLowerCase() + " " ] =
									( responseHeaders[ match[ 1 ].toLowerCase() + " " ] || [] )
										.concat( match[ 2 ] );
							}
						}
						match = responseHeaders[ key.toLowerCase() + " " ];
					}
					return match == null ? null : match.join( ", " );
				},

				// Raw string
				getAllResponseHeaders: function() {
					return completed ? responseHeadersString : null;
				},

				// Caches the header
				setRequestHeader: function( name, value ) {
					if ( completed == null ) {
						name = requestHeadersNames[ name.toLowerCase() ] =
							requestHeadersNames[ name.toLowerCase() ] || name;
						requestHeaders[ name ] = value;
					}
					return this;
				},

				// Overrides response content-type header
				overrideMimeType: function( type ) {
					if ( completed == null ) {
						s.mimeType = type;
					}
					return this;
				},

				// Status-dependent callbacks
				statusCode: function( map ) {
					var code;
					if ( map ) {
						if ( completed ) {

							// Execute the appropriate callbacks
							jqXHR.always( map[ jqXHR.status ] );
						} else {

							// Lazy-add the new callbacks in a way that preserves old ones
							for ( code in map ) {
								statusCode[ code ] = [ statusCode[ code ], map[ code ] ];
							}
						}
					}
					return this;
				},

				// Cancel the request
				abort: function( statusText ) {
					var finalText = statusText || strAbort;
					if ( transport ) {
						transport.abort( finalText );
					}
					done( 0, finalText );
					return this;
				}
			};

		// Attach deferreds
		deferred.promise( jqXHR );

		// Add protocol if not provided (prefilters might expect it)
		// Handle falsy url in the settings object (#10093: consistency with old signature)
		// We also use the url parameter if available
		s.url = ( ( url || s.url || location.href ) + "" )
			.replace( rprotocol, location.protocol + "//" );

		// Alias method option to type as per ticket #12004
		s.type = options.method || options.type || s.method || s.type;

		// Extract dataTypes list
		s.dataTypes = ( s.dataType || "*" ).toLowerCase().match( rnothtmlwhite ) || [ "" ];

		// A cross-domain request is in order when the origin doesn't match the current origin.
		if ( s.crossDomain == null ) {
			urlAnchor = document.createElement( "a" );

			// Support: IE <=8 - 11, Edge 12 - 15
			// IE throws exception on accessing the href property if url is malformed,
			// e.g. http://example.com:80x/
			try {
				urlAnchor.href = s.url;

				// Support: IE <=8 - 11 only
				// Anchor's host property isn't correctly set when s.url is relative
				urlAnchor.href = urlAnchor.href;
				s.crossDomain = originAnchor.protocol + "//" + originAnchor.host !==
					urlAnchor.protocol + "//" + urlAnchor.host;
			} catch ( e ) {

				// If there is an error parsing the URL, assume it is crossDomain,
				// it can be rejected by the transport if it is invalid
				s.crossDomain = true;
			}
		}

		// Convert data if not already a string
		if ( s.data && s.processData && typeof s.data !== "string" ) {
			s.data = jQuery.param( s.data, s.traditional );
		}

		// Apply prefilters
		inspectPrefiltersOrTransports( prefilters, s, options, jqXHR );

		// If request was aborted inside a prefilter, stop there
		if ( completed ) {
			return jqXHR;
		}

		// We can fire global events as of now if asked to
		// Don't fire events if jQuery.event is undefined in an AMD-usage scenario (#15118)
		fireGlobals = jQuery.event && s.global;

		// Watch for a new set of requests
		if ( fireGlobals && jQuery.active++ === 0 ) {
			jQuery.event.trigger( "ajaxStart" );
		}

		// Uppercase the type
		s.type = s.type.toUpperCase();

		// Determine if request has content
		s.hasContent = !rnoContent.test( s.type );

		// Save the URL in case we're toying with the If-Modified-Since
		// and/or If-None-Match header later on
		// Remove hash to simplify url manipulation
		cacheURL = s.url.replace( rhash, "" );

		// More options handling for requests with no content
		if ( !s.hasContent ) {

			// Remember the hash so we can put it back
			uncached = s.url.slice( cacheURL.length );

			// If data is available and should be processed, append data to url
			if ( s.data && ( s.processData || typeof s.data === "string" ) ) {
				cacheURL += ( rquery.test( cacheURL ) ? "&" : "?" ) + s.data;

				// #9682: remove data so that it's not used in an eventual retry
				delete s.data;
			}

			// Add or update anti-cache param if needed
			if ( s.cache === false ) {
				cacheURL = cacheURL.replace( rantiCache, "$1" );
				uncached = ( rquery.test( cacheURL ) ? "&" : "?" ) + "_=" + ( nonce.guid++ ) +
					uncached;
			}

			// Put hash and anti-cache on the URL that will be requested (gh-1732)
			s.url = cacheURL + uncached;

		// Change '%20' to '+' if this is encoded form body content (gh-2658)
		} else if ( s.data && s.processData &&
			( s.contentType || "" ).indexOf( "application/x-www-form-urlencoded" ) === 0 ) {
			s.data = s.data.replace( r20, "+" );
		}

		// Set the If-Modified-Since and/or If-None-Match header, if in ifModified mode.
		if ( s.ifModified ) {
			if ( jQuery.lastModified[ cacheURL ] ) {
				jqXHR.setRequestHeader( "If-Modified-Since", jQuery.lastModified[ cacheURL ] );
			}
			if ( jQuery.etag[ cacheURL ] ) {
				jqXHR.setRequestHeader( "If-None-Match", jQuery.etag[ cacheURL ] );
			}
		}

		// Set the correct header, if data is being sent
		if ( s.data && s.hasContent && s.contentType !== false || options.contentType ) {
			jqXHR.setRequestHeader( "Content-Type", s.contentType );
		}

		// Set the Accepts header for the server, depending on the dataType
		jqXHR.setRequestHeader(
			"Accept",
			s.dataTypes[ 0 ] && s.accepts[ s.dataTypes[ 0 ] ] ?
				s.accepts[ s.dataTypes[ 0 ] ] +
					( s.dataTypes[ 0 ] !== "*" ? ", " + allTypes + "; q=0.01" : "" ) :
				s.accepts[ "*" ]
		);

		// Check for headers option
		for ( i in s.headers ) {
			jqXHR.setRequestHeader( i, s.headers[ i ] );
		}

		// Allow custom headers/mimetypes and early abort
		if ( s.beforeSend &&
			( s.beforeSend.call( callbackContext, jqXHR, s ) === false || completed ) ) {

			// Abort if not done already and return
			return jqXHR.abort();
		}

		// Aborting is no longer a cancellation
		strAbort = "abort";

		// Install callbacks on deferreds
		completeDeferred.add( s.complete );
		jqXHR.done( s.success );
		jqXHR.fail( s.error );

		// Get transport
		transport = inspectPrefiltersOrTransports( transports, s, options, jqXHR );

		// If no transport, we auto-abort
		if ( !transport ) {
			done( -1, "No Transport" );
		} else {
			jqXHR.readyState = 1;

			// Send global event
			if ( fireGlobals ) {
				globalEventContext.trigger( "ajaxSend", [ jqXHR, s ] );
			}

			// If request was aborted inside ajaxSend, stop there
			if ( completed ) {
				return jqXHR;
			}

			// Timeout
			if ( s.async && s.timeout > 0 ) {
				timeoutTimer = window.setTimeout( function() {
					jqXHR.abort( "timeout" );
				}, s.timeout );
			}

			try {
				completed = false;
				transport.send( requestHeaders, done );
			} catch ( e ) {

				// Rethrow post-completion exceptions
				if ( completed ) {
					throw e;
				}

				// Propagate others as results
				done( -1, e );
			}
		}

		// Callback for when everything is done
		function done( status, nativeStatusText, responses, headers ) {
			var isSuccess, success, error, response, modified,
				statusText = nativeStatusText;

			// Ignore repeat invocations
			if ( completed ) {
				return;
			}

			completed = true;

			// Clear timeout if it exists
			if ( timeoutTimer ) {
				window.clearTimeout( timeoutTimer );
			}

			// Dereference transport for early garbage collection
			// (no matter how long the jqXHR object will be used)
			transport = undefined;

			// Cache response headers
			responseHeadersString = headers || "";

			// Set readyState
			jqXHR.readyState = status > 0 ? 4 : 0;

			// Determine if successful
			isSuccess = status >= 200 && status < 300 || status === 304;

			// Get response data
			if ( responses ) {
				response = ajaxHandleResponses( s, jqXHR, responses );
			}

			// Use a noop converter for missing script
			if ( !isSuccess && jQuery.inArray( "script", s.dataTypes ) > -1 ) {
				s.converters[ "text script" ] = function() {};
			}

			// Convert no matter what (that way responseXXX fields are always set)
			response = ajaxConvert( s, response, jqXHR, isSuccess );

			// If successful, handle type chaining
			if ( isSuccess ) {

				// Set the If-Modified-Since and/or If-None-Match header, if in ifModified mode.
				if ( s.ifModified ) {
					modified = jqXHR.getResponseHeader( "Last-Modified" );
					if ( modified ) {
						jQuery.lastModified[ cacheURL ] = modified;
					}
					modified = jqXHR.getResponseHeader( "etag" );
					if ( modified ) {
						jQuery.etag[ cacheURL ] = modified;
					}
				}

				// if no content
				if ( status === 204 || s.type === "HEAD" ) {
					statusText = "nocontent";

				// if not modified
				} else if ( status === 304 ) {
					statusText = "notmodified";

				// If we have data, let's convert it
				} else {
					statusText = response.state;
					success = response.data;
					error = response.error;
					isSuccess = !error;
				}
			} else {

				// Extract error from statusText and normalize for non-aborts
				error = statusText;
				if ( status || !statusText ) {
					statusText = "error";
					if ( status < 0 ) {
						status = 0;
					}
				}
			}

			// Set data for the fake xhr object
			jqXHR.status = status;
			jqXHR.statusText = ( nativeStatusText || statusText ) + "";

			// Success/Error
			if ( isSuccess ) {
				deferred.resolveWith( callbackContext, [ success, statusText, jqXHR ] );
			} else {
				deferred.rejectWith( callbackContext, [ jqXHR, statusText, error ] );
			}

			// Status-dependent callbacks
			jqXHR.statusCode( statusCode );
			statusCode = undefined;

			if ( fireGlobals ) {
				globalEventContext.trigger( isSuccess ? "ajaxSuccess" : "ajaxError",
					[ jqXHR, s, isSuccess ? success : error ] );
			}

			// Complete
			completeDeferred.fireWith( callbackContext, [ jqXHR, statusText ] );

			if ( fireGlobals ) {
				globalEventContext.trigger( "ajaxComplete", [ jqXHR, s ] );

				// Handle the global AJAX counter
				if ( !( --jQuery.active ) ) {
					jQuery.event.trigger( "ajaxStop" );
				}
			}
		}

		return jqXHR;
	},

	getJSON: function( url, data, callback ) {
		return jQuery.get( url, data, callback, "json" );
	},

	getScript: function( url, callback ) {
		return jQuery.get( url, undefined, callback, "script" );
	}
} );

jQuery.each( [ "get", "post" ], function( _i, method ) {
	jQuery[ method ] = function( url, data, callback, type ) {

		// Shift arguments if data argument was omitted
		if ( isFunction( data ) ) {
			type = type || callback;
			callback = data;
			data = undefined;
		}

		// The url can be an options object (which then must have .url)
		return jQuery.ajax( jQuery.extend( {
			url: url,
			type: method,
			dataType: type,
			data: data,
			success: callback
		}, jQuery.isPlainObject( url ) && url ) );
	};
} );

jQuery.ajaxPrefilter( function( s ) {
	var i;
	for ( i in s.headers ) {
		if ( i.toLowerCase() === "content-type" ) {
			s.contentType = s.headers[ i ] || "";
		}
	}
} );


jQuery._evalUrl = function( url, options, doc ) {
	return jQuery.ajax( {
		url: url,

		// Make this explicit, since user can override this through ajaxSetup (#11264)
		type: "GET",
		dataType: "script",
		cache: true,
		async: false,
		global: false,

		// Only evaluate the response if it is successful (gh-4126)
		// dataFilter is not invoked for failure responses, so using it instead
		// of the default converter is kludgy but it works.
		converters: {
			"text script": function() {}
		},
		dataFilter: function( response ) {
			jQuery.globalEval( response, options, doc );
		}
	} );
};


jQuery.fn.extend( {
	wrapAll: function( html ) {
		var wrap;

		if ( this[ 0 ] ) {
			if ( isFunction( html ) ) {
				html = html.call( this[ 0 ] );
			}

			// The elements to wrap the target around
			wrap = jQuery( html, this[ 0 ].ownerDocument ).eq( 0 ).clone( true );

			if ( this[ 0 ].parentNode ) {
				wrap.insertBefore( this[ 0 ] );
			}

			wrap.map( function() {
				var elem = this;

				while ( elem.firstElementChild ) {
					elem = elem.firstElementChild;
				}

				return elem;
			} ).append( this );
		}

		return this;
	},

	wrapInner: function( html ) {
		if ( isFunction( html ) ) {
			return this.each( function( i ) {
				jQuery( this ).wrapInner( html.call( this, i ) );
			} );
		}

		return this.each( function() {
			var self = jQuery( this ),
				contents = self.contents();

			if ( contents.length ) {
				contents.wrapAll( html );

			} else {
				self.append( html );
			}
		} );
	},

	wrap: function( html ) {
		var htmlIsFunction = isFunction( html );

		return this.each( function( i ) {
			jQuery( this ).wrapAll( htmlIsFunction ? html.call( this, i ) : html );
		} );
	},

	unwrap: function( selector ) {
		this.parent( selector ).not( "body" ).each( function() {
			jQuery( this ).replaceWith( this.childNodes );
		} );
		return this;
	}
} );


jQuery.expr.pseudos.hidden = function( elem ) {
	return !jQuery.expr.pseudos.visible( elem );
};
jQuery.expr.pseudos.visible = function( elem ) {
	return !!( elem.offsetWidth || elem.offsetHeight || elem.getClientRects().length );
};




jQuery.ajaxSettings.xhr = function() {
	try {
		return new window.XMLHttpRequest();
	} catch ( e ) {}
};

var xhrSuccessStatus = {

		// File protocol always yields status code 0, assume 200
		0: 200,

		// Support: IE <=9 only
		// #1450: sometimes IE returns 1223 when it should be 204
		1223: 204
	},
	xhrSupported = jQuery.ajaxSettings.xhr();

support.cors = !!xhrSupported && ( "withCredentials" in xhrSupported );
support.ajax = xhrSupported = !!xhrSupported;

jQuery.ajaxTransport( function( options ) {
	var callback, errorCallback;

	// Cross domain only allowed if supported through XMLHttpRequest
	if ( support.cors || xhrSupported && !options.crossDomain ) {
		return {
			send: function( headers, complete ) {
				var i,
					xhr = options.xhr();

				xhr.open(
					options.type,
					options.url,
					options.async,
					options.username,
					options.password
				);

				// Apply custom fields if provided
				if ( options.xhrFields ) {
					for ( i in options.xhrFields ) {
						xhr[ i ] = options.xhrFields[ i ];
					}
				}

				// Override mime type if needed
				if ( options.mimeType && xhr.overrideMimeType ) {
					xhr.overrideMimeType( options.mimeType );
				}

				// X-Requested-With header
				// For cross-domain requests, seeing as conditions for a preflight are
				// akin to a jigsaw puzzle, we simply never set it to be sure.
				// (it can always be set on a per-request basis or even using ajaxSetup)
				// For same-domain requests, won't change header if already provided.
				if ( !options.crossDomain && !headers[ "X-Requested-With" ] ) {
					headers[ "X-Requested-With" ] = "XMLHttpRequest";
				}

				// Set headers
				for ( i in headers ) {
					xhr.setRequestHeader( i, headers[ i ] );
				}

				// Callback
				callback = function( type ) {
					return function() {
						if ( callback ) {
							callback = errorCallback = xhr.onload =
								xhr.onerror = xhr.onabort = xhr.ontimeout =
									xhr.onreadystatechange = null;

							if ( type === "abort" ) {
								xhr.abort();
							} else if ( type === "error" ) {

								// Support: IE <=9 only
								// On a manual native abort, IE9 throws
								// errors on any property access that is not readyState
								if ( typeof xhr.status !== "number" ) {
									complete( 0, "error" );
								} else {
									complete(

										// File: protocol always yields status 0; see #8605, #14207
										xhr.status,
										xhr.statusText
									);
								}
							} else {
								complete(
									xhrSuccessStatus[ xhr.status ] || xhr.status,
									xhr.statusText,

									// Support: IE <=9 only
									// IE9 has no XHR2 but throws on binary (trac-11426)
									// For XHR2 non-text, let the caller handle it (gh-2498)
									( xhr.responseType || "text" ) !== "text"  ||
									typeof xhr.responseText !== "string" ?
										{ binary: xhr.response } :
										{ text: xhr.responseText },
									xhr.getAllResponseHeaders()
								);
							}
						}
					};
				};

				// Listen to events
				xhr.onload = callback();
				errorCallback = xhr.onerror = xhr.ontimeout = callback( "error" );

				// Support: IE 9 only
				// Use onreadystatechange to replace onabort
				// to handle uncaught aborts
				if ( xhr.onabort !== undefined ) {
					xhr.onabort = errorCallback;
				} else {
					xhr.onreadystatechange = function() {

						// Check readyState before timeout as it changes
						if ( xhr.readyState === 4 ) {

							// Allow onerror to be called first,
							// but that will not handle a native abort
							// Also, save errorCallback to a variable
							// as xhr.onerror cannot be accessed
							window.setTimeout( function() {
								if ( callback ) {
									errorCallback();
								}
							} );
						}
					};
				}

				// Create the abort callback
				callback = callback( "abort" );

				try {

					// Do send the request (this may raise an exception)
					xhr.send( options.hasContent && options.data || null );
				} catch ( e ) {

					// #14683: Only rethrow if this hasn't been notified as an error yet
					if ( callback ) {
						throw e;
					}
				}
			},

			abort: function() {
				if ( callback ) {
					callback();
				}
			}
		};
	}
} );




// Prevent auto-execution of scripts when no explicit dataType was provided (See gh-2432)
jQuery.ajaxPrefilter( function( s ) {
	if ( s.crossDomain ) {
		s.contents.script = false;
	}
} );

// Install script dataType
jQuery.ajaxSetup( {
	accepts: {
		script: "text/javascript, application/javascript, " +
			"application/ecmascript, application/x-ecmascript"
	},
	contents: {
		script: /\b(?:java|ecma)script\b/
	},
	converters: {
		"text script": function( text ) {
			jQuery.globalEval( text );
			return text;
		}
	}
} );

// Handle cache's special case and crossDomain
jQuery.ajaxPrefilter( "script", function( s ) {
	if ( s.cache === undefined ) {
		s.cache = false;
	}
	if ( s.crossDomain ) {
		s.type = "GET";
	}
} );

// Bind script tag hack transport
jQuery.ajaxTransport( "script", function( s ) {

	// This transport only deals with cross domain or forced-by-attrs requests
	if ( s.crossDomain || s.scriptAttrs ) {
		var script, callback;
		return {
			send: function( _, complete ) {
				script = jQuery( "<script>" )
					.attr( s.scriptAttrs || {} )
					.prop( { charset: s.scriptCharset, src: s.url } )
					.on( "load error", callback = function( evt ) {
						script.remove();
						callback = null;
						if ( evt ) {
							complete( evt.type === "error" ? 404 : 200, evt.type );
						}
					} );

				// Use native DOM manipulation to avoid our domManip AJAX trickery
				document.head.appendChild( script[ 0 ] );
			},
			abort: function() {
				if ( callback ) {
					callback();
				}
			}
		};
	}
} );




var oldCallbacks = [],
	rjsonp = /(=)\?(?=&|$)|\?\?/;

// Default jsonp settings
jQuery.ajaxSetup( {
	jsonp: "callback",
	jsonpCallback: function() {
		var callback = oldCallbacks.pop() || ( jQuery.expando + "_" + ( nonce.guid++ ) );
		this[ callback ] = true;
		return callback;
	}
} );

// Detect, normalize options and install callbacks for jsonp requests
jQuery.ajaxPrefilter( "json jsonp", function( s, originalSettings, jqXHR ) {

	var callbackName, overwritten, responseContainer,
		jsonProp = s.jsonp !== false && ( rjsonp.test( s.url ) ?
			"url" :
			typeof s.data === "string" &&
				( s.contentType || "" )
					.indexOf( "application/x-www-form-urlencoded" ) === 0 &&
				rjsonp.test( s.data ) && "data"
		);

	// Handle iff the expected data type is "jsonp" or we have a parameter to set
	if ( jsonProp || s.dataTypes[ 0 ] === "jsonp" ) {

		// Get callback name, remembering preexisting value associated with it
		callbackName = s.jsonpCallback = isFunction( s.jsonpCallback ) ?
			s.jsonpCallback() :
			s.jsonpCallback;

		// Insert callback into url or form data
		if ( jsonProp ) {
			s[ jsonProp ] = s[ jsonProp ].replace( rjsonp, "$1" + callbackName );
		} else if ( s.jsonp !== false ) {
			s.url += ( rquery.test( s.url ) ? "&" : "?" ) + s.jsonp + "=" + callbackName;
		}

		// Use data converter to retrieve json after script execution
		s.converters[ "script json" ] = function() {
			if ( !responseContainer ) {
				jQuery.error( callbackName + " was not called" );
			}
			return responseContainer[ 0 ];
		};

		// Force json dataType
		s.dataTypes[ 0 ] = "json";

		// Install callback
		overwritten = window[ callbackName ];
		window[ callbackName ] = function() {
			responseContainer = arguments;
		};

		// Clean-up function (fires after converters)
		jqXHR.always( function() {

			// If previous value didn't exist - remove it
			if ( overwritten === undefined ) {
				jQuery( window ).removeProp( callbackName );

			// Otherwise restore preexisting value
			} else {
				window[ callbackName ] = overwritten;
			}

			// Save back as free
			if ( s[ callbackName ] ) {

				// Make sure that re-using the options doesn't screw things around
				s.jsonpCallback = originalSettings.jsonpCallback;

				// Save the callback name for future use
				oldCallbacks.push( callbackName );
			}

			// Call if it was a function and we have a response
			if ( responseContainer && isFunction( overwritten ) ) {
				overwritten( responseContainer[ 0 ] );
			}

			responseContainer = overwritten = undefined;
		} );

		// Delegate to script
		return "script";
	}
} );




// Support: Safari 8 only
// In Safari 8 documents created via document.implementation.createHTMLDocument
// collapse sibling forms: the second one becomes a child of the first one.
// Because of that, this security measure has to be disabled in Safari 8.
// https://bugs.webkit.org/show_bug.cgi?id=137337
support.createHTMLDocument = ( function() {
	var body = document.implementation.createHTMLDocument( "" ).body;
	body.innerHTML = "<form></form><form></form>";
	return body.childNodes.length === 2;
} )();


// Argument "data" should be string of html
// context (optional): If specified, the fragment will be created in this context,
// defaults to document
// keepScripts (optional): If true, will include scripts passed in the html string
jQuery.parseHTML = function( data, context, keepScripts ) {
	if ( typeof data !== "string" ) {
		return [];
	}
	if ( typeof context === "boolean" ) {
		keepScripts = context;
		context = false;
	}

	var base, parsed, scripts;

	if ( !context ) {

		// Stop scripts or inline event handlers from being executed immediately
		// by using document.implementation
		if ( support.createHTMLDocument ) {
			context = document.implementation.createHTMLDocument( "" );

			// Set the base href for the created document
			// so any parsed elements with URLs
			// are based on the document's URL (gh-2965)
			base = context.createElement( "base" );
			base.href = document.location.href;
			context.head.appendChild( base );
		} else {
			context = document;
		}
	}

	parsed = rsingleTag.exec( data );
	scripts = !keepScripts && [];

	// Single tag
	if ( parsed ) {
		return [ context.createElement( parsed[ 1 ] ) ];
	}

	parsed = buildFragment( [ data ], context, scripts );

	if ( scripts && scripts.length ) {
		jQuery( scripts ).remove();
	}

	return jQuery.merge( [], parsed.childNodes );
};


/**
 * Load a url into a page
 */
jQuery.fn.load = function( url, params, callback ) {
	var selector, type, response,
		self = this,
		off = url.indexOf( " " );

	if ( off > -1 ) {
		selector = stripAndCollapse( url.slice( off ) );
		url = url.slice( 0, off );
	}

	// If it's a function
	if ( isFunction( params ) ) {

		// We assume that it's the callback
		callback = params;
		params = undefined;

	// Otherwise, build a param string
	} else if ( params && typeof params === "object" ) {
		type = "POST";
	}

	// If we have elements to modify, make the request
	if ( self.length > 0 ) {
		jQuery.ajax( {
			url: url,

			// If "type" variable is undefined, then "GET" method will be used.
			// Make value of this field explicit since
			// user can override it through ajaxSetup method
			type: type || "GET",
			dataType: "html",
			data: params
		} ).done( function( responseText ) {

			// Save response for use in complete callback
			response = arguments;

			self.html( selector ?

				// If a selector was specified, locate the right elements in a dummy div
				// Exclude scripts to avoid IE 'Permission Denied' errors
				jQuery( "<div>" ).append( jQuery.parseHTML( responseText ) ).find( selector ) :

				// Otherwise use the full result
				responseText );

		// If the request succeeds, this function gets "data", "status", "jqXHR"
		// but they are ignored because response was set above.
		// If it fails, this function gets "jqXHR", "status", "error"
		} ).always( callback && function( jqXHR, status ) {
			self.each( function() {
				callback.apply( this, response || [ jqXHR.responseText, status, jqXHR ] );
			} );
		} );
	}

	return this;
};




jQuery.expr.pseudos.animated = function( elem ) {
	return jQuery.grep( jQuery.timers, function( fn ) {
		return elem === fn.elem;
	} ).length;
};




jQuery.offset = {
	setOffset: function( elem, options, i ) {
		var curPosition, curLeft, curCSSTop, curTop, curOffset, curCSSLeft, calculatePosition,
			position = jQuery.css( elem, "position" ),
			curElem = jQuery( elem ),
			props = {};

		// Set position first, in-case top/left are set even on static elem
		if ( position === "static" ) {
			elem.style.position = "relative";
		}

		curOffset = curElem.offset();
		curCSSTop = jQuery.css( elem, "top" );
		curCSSLeft = jQuery.css( elem, "left" );
		calculatePosition = ( position === "absolute" || position === "fixed" ) &&
			( curCSSTop + curCSSLeft ).indexOf( "auto" ) > -1;

		// Need to be able to calculate position if either
		// top or left is auto and position is either absolute or fixed
		if ( calculatePosition ) {
			curPosition = curElem.position();
			curTop = curPosition.top;
			curLeft = curPosition.left;

		} else {
			curTop = parseFloat( curCSSTop ) || 0;
			curLeft = parseFloat( curCSSLeft ) || 0;
		}

		if ( isFunction( options ) ) {

			// Use jQuery.extend here to allow modification of coordinates argument (gh-1848)
			options = options.call( elem, i, jQuery.extend( {}, curOffset ) );
		}

		if ( options.top != null ) {
			props.top = ( options.top - curOffset.top ) + curTop;
		}
		if ( options.left != null ) {
			props.left = ( options.left - curOffset.left ) + curLeft;
		}

		if ( "using" in options ) {
			options.using.call( elem, props );

		} else {
			if ( typeof props.top === "number" ) {
				props.top += "px";
			}
			if ( typeof props.left === "number" ) {
				props.left += "px";
			}
			curElem.css( props );
		}
	}
};

jQuery.fn.extend( {

	// offset() relates an element's border box to the document origin
	offset: function( options ) {

		// Preserve chaining for setter
		if ( arguments.length ) {
			return options === undefined ?
				this :
				this.each( function( i ) {
					jQuery.offset.setOffset( this, options, i );
				} );
		}

		var rect, win,
			elem = this[ 0 ];

		if ( !elem ) {
			return;
		}

		// Return zeros for disconnected and hidden (display: none) elements (gh-2310)
		// Support: IE <=11 only
		// Running getBoundingClientRect on a
		// disconnected node in IE throws an error
		if ( !elem.getClientRects().length ) {
			return { top: 0, left: 0 };
		}

		// Get document-relative position by adding viewport scroll to viewport-relative gBCR
		rect = elem.getBoundingClientRect();
		win = elem.ownerDocument.defaultView;
		return {
			top: rect.top + win.pageYOffset,
			left: rect.left + win.pageXOffset
		};
	},

	// position() relates an element's margin box to its offset parent's padding box
	// This corresponds to the behavior of CSS absolute positioning
	position: function() {
		if ( !this[ 0 ] ) {
			return;
		}

		var offsetParent, offset, doc,
			elem = this[ 0 ],
			parentOffset = { top: 0, left: 0 };

		// position:fixed elements are offset from the viewport, which itself always has zero offset
		if ( jQuery.css( elem, "position" ) === "fixed" ) {

			// Assume position:fixed implies availability of getBoundingClientRect
			offset = elem.getBoundingClientRect();

		} else {
			offset = this.offset();

			// Account for the *real* offset parent, which can be the document or its root element
			// when a statically positioned element is identified
			doc = elem.ownerDocument;
			offsetParent = elem.offsetParent || doc.documentElement;
			while ( offsetParent &&
				( offsetParent === doc.body || offsetParent === doc.documentElement ) &&
				jQuery.css( offsetParent, "position" ) === "static" ) {

				offsetParent = offsetParent.parentNode;
			}
			if ( offsetParent && offsetParent !== elem && offsetParent.nodeType === 1 ) {

				// Incorporate borders into its offset, since they are outside its content origin
				parentOffset = jQuery( offsetParent ).offset();
				parentOffset.top += jQuery.css( offsetParent, "borderTopWidth", true );
				parentOffset.left += jQuery.css( offsetParent, "borderLeftWidth", true );
			}
		}

		// Subtract parent offsets and element margins
		return {
			top: offset.top - parentOffset.top - jQuery.css( elem, "marginTop", true ),
			left: offset.left - parentOffset.left - jQuery.css( elem, "marginLeft", true )
		};
	},

	// This method will return documentElement in the following cases:
	// 1) For the element inside the iframe without offsetParent, this method will return
	//    documentElement of the parent window
	// 2) For the hidden or detached element
	// 3) For body or html element, i.e. in case of the html node - it will return itself
	//
	// but those exceptions were never presented as a real life use-cases
	// and might be considered as more preferable results.
	//
	// This logic, however, is not guaranteed and can change at any point in the future
	offsetParent: function() {
		return this.map( function() {
			var offsetParent = this.offsetParent;

			while ( offsetParent && jQuery.css( offsetParent, "position" ) === "static" ) {
				offsetParent = offsetParent.offsetParent;
			}

			return offsetParent || documentElement;
		} );
	}
} );

// Create scrollLeft and scrollTop methods
jQuery.each( { scrollLeft: "pageXOffset", scrollTop: "pageYOffset" }, function( method, prop ) {
	var top = "pageYOffset" === prop;

	jQuery.fn[ method ] = function( val ) {
		return access( this, function( elem, method, val ) {

			// Coalesce documents and windows
			var win;
			if ( isWindow( elem ) ) {
				win = elem;
			} else if ( elem.nodeType === 9 ) {
				win = elem.defaultView;
			}

			if ( val === undefined ) {
				return win ? win[ prop ] : elem[ method ];
			}

			if ( win ) {
				win.scrollTo(
					!top ? val : win.pageXOffset,
					top ? val : win.pageYOffset
				);

			} else {
				elem[ method ] = val;
			}
		}, method, val, arguments.length );
	};
} );

// Support: Safari <=7 - 9.1, Chrome <=37 - 49
// Add the top/left cssHooks using jQuery.fn.position
// Webkit bug: https://bugs.webkit.org/show_bug.cgi?id=29084
// Blink bug: https://bugs.chromium.org/p/chromium/issues/detail?id=589347
// getComputedStyle returns percent when specified for top/left/bottom/right;
// rather than make the css module depend on the offset module, just check for it here
jQuery.each( [ "top", "left" ], function( _i, prop ) {
	jQuery.cssHooks[ prop ] = addGetHookIf( support.pixelPosition,
		function( elem, computed ) {
			if ( computed ) {
				computed = curCSS( elem, prop );

				// If curCSS returns percentage, fallback to offset
				return rnumnonpx.test( computed ) ?
					jQuery( elem ).position()[ prop ] + "px" :
					computed;
			}
		}
	);
} );


// Create innerHeight, innerWidth, height, width, outerHeight and outerWidth methods
jQuery.each( { Height: "height", Width: "width" }, function( name, type ) {
	jQuery.each( { padding: "inner" + name, content: type, "": "outer" + name },
		function( defaultExtra, funcName ) {

		// Margin is only for outerHeight, outerWidth
		jQuery.fn[ funcName ] = function( margin, value ) {
			var chainable = arguments.length && ( defaultExtra || typeof margin !== "boolean" ),
				extra = defaultExtra || ( margin === true || value === true ? "margin" : "border" );

			return access( this, function( elem, type, value ) {
				var doc;

				if ( isWindow( elem ) ) {

					// $( window ).outerWidth/Height return w/h including scrollbars (gh-1729)
					return funcName.indexOf( "outer" ) === 0 ?
						elem[ "inner" + name ] :
						elem.document.documentElement[ "client" + name ];
				}

				// Get document width or height
				if ( elem.nodeType === 9 ) {
					doc = elem.documentElement;

					// Either scroll[Width/Height] or offset[Width/Height] or client[Width/Height],
					// whichever is greatest
					return Math.max(
						elem.body[ "scroll" + name ], doc[ "scroll" + name ],
						elem.body[ "offset" + name ], doc[ "offset" + name ],
						doc[ "client" + name ]
					);
				}

				return value === undefined ?

					// Get width or height on the element, requesting but not forcing parseFloat
					jQuery.css( elem, type, extra ) :

					// Set width or height on the element
					jQuery.style( elem, type, value, extra );
			}, type, chainable ? margin : undefined, chainable );
		};
	} );
} );


jQuery.each( [
	"ajaxStart",
	"ajaxStop",
	"ajaxComplete",
	"ajaxError",
	"ajaxSuccess",
	"ajaxSend"
], function( _i, type ) {
	jQuery.fn[ type ] = function( fn ) {
		return this.on( type, fn );
	};
} );




jQuery.fn.extend( {

	bind: function( types, data, fn ) {
		return this.on( types, null, data, fn );
	},
	unbind: function( types, fn ) {
		return this.off( types, null, fn );
	},

	delegate: function( selector, types, data, fn ) {
		return this.on( types, selector, data, fn );
	},
	undelegate: function( selector, types, fn ) {

		// ( namespace ) or ( selector, types [, fn] )
		return arguments.length === 1 ?
			this.off( selector, "**" ) :
			this.off( types, selector || "**", fn );
	},

	hover: function( fnOver, fnOut ) {
		return this.mouseenter( fnOver ).mouseleave( fnOut || fnOver );
	}
} );

jQuery.each( ( "blur focus focusin focusout resize scroll click dblclick " +
	"mousedown mouseup mousemove mouseover mouseout mouseenter mouseleave " +
	"change select submit keydown keypress keyup contextmenu" ).split( " " ),
	function( _i, name ) {

		// Handle event binding
		jQuery.fn[ name ] = function( data, fn ) {
			return arguments.length > 0 ?
				this.on( name, null, data, fn ) :
				this.trigger( name );
		};
	} );




// Support: Android <=4.0 only
// Make sure we trim BOM and NBSP
var rtrim = /^[\s\uFEFF\xA0]+|[\s\uFEFF\xA0]+$/g;

// Bind a function to a context, optionally partially applying any
// arguments.
// jQuery.proxy is deprecated to promote standards (specifically Function#bind)
// However, it is not slated for removal any time soon
jQuery.proxy = function( fn, context ) {
	var tmp, args, proxy;

	if ( typeof context === "string" ) {
		tmp = fn[ context ];
		context = fn;
		fn = tmp;
	}

	// Quick check to determine if target is callable, in the spec
	// this throws a TypeError, but we will just return undefined.
	if ( !isFunction( fn ) ) {
		return undefined;
	}

	// Simulated bind
	args = slice.call( arguments, 2 );
	proxy = function() {
		return fn.apply( context || this, args.concat( slice.call( arguments ) ) );
	};

	// Set the guid of unique handler to the same of original handler, so it can be removed
	proxy.guid = fn.guid = fn.guid || jQuery.guid++;

	return proxy;
};

jQuery.holdReady = function( hold ) {
	if ( hold ) {
		jQuery.readyWait++;
	} else {
		jQuery.ready( true );
	}
};
jQuery.isArray = Array.isArray;
jQuery.parseJSON = JSON.parse;
jQuery.nodeName = nodeName;
jQuery.isFunction = isFunction;
jQuery.isWindow = isWindow;
jQuery.camelCase = camelCase;
jQuery.type = toType;

jQuery.now = Date.now;

jQuery.isNumeric = function( obj ) {

	// As of jQuery 3.0, isNumeric is limited to
	// strings and numbers (primitives or objects)
	// that can be coerced to finite numbers (gh-2662)
	var type = jQuery.type( obj );
	return ( type === "number" || type === "string" ) &&

		// parseFloat NaNs numeric-cast false positives ("")
		// ...but misinterprets leading-number strings, particularly hex literals ("0x...")
		// subtraction forces infinities to NaN
		!isNaN( obj - parseFloat( obj ) );
};

jQuery.trim = function( text ) {
	return text == null ?
		"" :
		( text + "" ).replace( rtrim, "" );
};



// Register as a named AMD module, since jQuery can be concatenated with other
// files that may use define, but not via a proper concatenation script that
// understands anonymous AMD modules. A named AMD is safest and most robust
// way to register. Lowercase jquery is used because AMD module names are
// derived from file names, and jQuery is normally delivered in a lowercase
// file name. Do this after creating the global so that if an AMD module wants
// to call noConflict to hide this version of jQuery, it will work.

// Note that for maximum portability, libraries that are not jQuery should
// declare themselves as anonymous modules, and avoid setting a global if an
// AMD loader is present. jQuery is a special case. For more information, see
// https://github.com/jrburke/requirejs/wiki/Updating-existing-libraries#wiki-anon

if ( true ) {
	!(__WEBPACK_AMD_DEFINE_ARRAY__ = [], __WEBPACK_AMD_DEFINE_RESULT__ = (function() {
		return jQuery;
	}).apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__),
				__WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
}




var

	// Map over jQuery in case of overwrite
	_jQuery = window.jQuery,

	// Map over the $ in case of overwrite
	_$ = window.$;

jQuery.noConflict = function( deep ) {
	if ( window.$ === jQuery ) {
		window.$ = _$;
	}

	if ( deep && window.jQuery === jQuery ) {
		window.jQuery = _jQuery;
	}

	return jQuery;
};

// Expose jQuery and $ identifiers, even in AMD
// (#7102#comment:10, https://github.com/jquery/jquery/pull/557)
// and CommonJS for browser emulators (#13566)
if ( typeof noGlobal === "undefined" ) {
	window.jQuery = window.$ = jQuery;
}




return jQuery;
} );


/***/ }),

/***/ "./node_modules/underscore/modules/index-all.js":
/*!******************************************************!*\
  !*** ./node_modules/underscore/modules/index-all.js ***!
  \******************************************************/
/*! exports provided: default, VERSION, iteratee, restArguments, each, forEach, map, collect, reduce, foldl, inject, reduceRight, foldr, find, detect, filter, select, reject, every, all, some, any, contains, includes, include, invoke, pluck, where, findWhere, max, min, shuffle, sample, sortBy, groupBy, indexBy, countBy, toArray, size, partition, first, head, take, initial, last, rest, tail, drop, compact, flatten, without, uniq, unique, union, intersection, difference, unzip, zip, object, findIndex, findLastIndex, sortedIndex, indexOf, lastIndexOf, range, chunk, bind, partial, bindAll, memoize, delay, defer, throttle, debounce, wrap, negate, compose, after, before, once, keys, allKeys, values, mapObject, pairs, invert, functions, methods, extend, extendOwn, assign, findKey, pick, omit, defaults, create, clone, tap, isMatch, isEqual, isEmpty, isElement, isArray, isObject, isArguments, isFunction, isString, isNumber, isDate, isRegExp, isError, isSymbol, isMap, isWeakMap, isSet, isWeakSet, isFinite, isNaN, isBoolean, isNull, isUndefined, has, identity, constant, noop, property, propertyOf, matcher, matches, times, random, now, escape, unescape, result, uniqueId, templateSettings, template, chain, mixin */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _index_default_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index-default.js */ "./node_modules/underscore/modules/index-default.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "default", function() { return _index_default_js__WEBPACK_IMPORTED_MODULE_0__["default"]; });

/* harmony import */ var _index_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./index.js */ "./node_modules/underscore/modules/index.js");
/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "VERSION", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["VERSION"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "iteratee", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["iteratee"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "restArguments", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["restArguments"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "each", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["each"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "forEach", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["forEach"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "map", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["map"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "collect", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["collect"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "reduce", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["reduce"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "foldl", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["foldl"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "inject", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["inject"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "reduceRight", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["reduceRight"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "foldr", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["foldr"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "find", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["find"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "detect", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["detect"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "filter", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["filter"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "select", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["select"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "reject", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["reject"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "every", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["every"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "all", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["all"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "some", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["some"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "any", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["any"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "contains", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["contains"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "includes", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["includes"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "include", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["include"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "invoke", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["invoke"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "pluck", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["pluck"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "where", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["where"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "findWhere", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["findWhere"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "max", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["max"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "min", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["min"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "shuffle", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["shuffle"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "sample", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["sample"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "sortBy", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["sortBy"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "groupBy", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["groupBy"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "indexBy", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["indexBy"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "countBy", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["countBy"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "toArray", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["toArray"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "size", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["size"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "partition", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["partition"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "first", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["first"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "head", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["head"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "take", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["take"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "initial", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["initial"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "last", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["last"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "rest", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["rest"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "tail", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["tail"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "drop", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["drop"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "compact", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["compact"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "flatten", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["flatten"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "without", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["without"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "uniq", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["uniq"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "unique", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["unique"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "union", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["union"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "intersection", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["intersection"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "difference", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["difference"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "unzip", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["unzip"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "zip", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["zip"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "object", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["object"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "findIndex", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["findIndex"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "findLastIndex", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["findLastIndex"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "sortedIndex", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["sortedIndex"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "indexOf", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["indexOf"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "lastIndexOf", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["lastIndexOf"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "range", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["range"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "chunk", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["chunk"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "bind", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["bind"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "partial", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["partial"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "bindAll", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["bindAll"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "memoize", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["memoize"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "delay", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["delay"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "defer", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["defer"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "throttle", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["throttle"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "debounce", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["debounce"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "wrap", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["wrap"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "negate", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["negate"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "compose", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["compose"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "after", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["after"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "before", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["before"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "once", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["once"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "keys", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["keys"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "allKeys", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["allKeys"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "values", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["values"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "mapObject", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["mapObject"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "pairs", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["pairs"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "invert", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["invert"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "functions", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["functions"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "methods", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["methods"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "extend", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["extend"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "extendOwn", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["extendOwn"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "assign", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["assign"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "findKey", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["findKey"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "pick", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["pick"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "omit", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["omit"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "defaults", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["defaults"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "create", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["create"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "clone", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["clone"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "tap", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["tap"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isMatch", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isMatch"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isEqual", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isEqual"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isEmpty", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isEmpty"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isElement", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isElement"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isArray", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isArray"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isObject", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isObject"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isArguments", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isArguments"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isFunction", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isFunction"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isString", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isString"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isNumber", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isNumber"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isDate", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isDate"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isRegExp", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isRegExp"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isError", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isError"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isSymbol", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isSymbol"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isMap", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isMap"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isWeakMap", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isWeakMap"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isSet", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isSet"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isWeakSet", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isWeakSet"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isFinite", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isFinite"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isNaN", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isNaN"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isBoolean", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isBoolean"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isNull", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isNull"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "isUndefined", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["isUndefined"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "has", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["has"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "identity", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["identity"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "constant", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["constant"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "noop", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["noop"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "property", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["property"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "propertyOf", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["propertyOf"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "matcher", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["matcher"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "matches", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["matches"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "times", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["times"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "random", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["random"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "now", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["now"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "escape", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["escape"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "unescape", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["unescape"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "result", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["result"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "uniqueId", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["uniqueId"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "templateSettings", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["templateSettings"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "template", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["template"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "chain", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["chain"]; });

/* harmony reexport (safe) */ __webpack_require__.d(__webpack_exports__, "mixin", function() { return _index_js__WEBPACK_IMPORTED_MODULE_1__["mixin"]; });





/***/ }),

/***/ "./node_modules/underscore/modules/index-default.js":
/*!**********************************************************!*\
  !*** ./node_modules/underscore/modules/index-default.js ***!
  \**********************************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _index_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./index.js */ "./node_modules/underscore/modules/index.js");



// Add all of the Underscore functions to the wrapper object.
var _ = Object(_index_js__WEBPACK_IMPORTED_MODULE_0__["mixin"])(_index_js__WEBPACK_IMPORTED_MODULE_0__);
// Legacy Node.js API
_._ = _;
// Export the Underscore API.
/* harmony default export */ __webpack_exports__["default"] = (_);


/***/ }),

/***/ "./node_modules/underscore/modules/index.js":
/*!**************************************************!*\
  !*** ./node_modules/underscore/modules/index.js ***!
  \**************************************************/
/*! exports provided: default, VERSION, iteratee, restArguments, each, forEach, map, collect, reduce, foldl, inject, reduceRight, foldr, find, detect, filter, select, reject, every, all, some, any, contains, includes, include, invoke, pluck, where, findWhere, max, min, shuffle, sample, sortBy, groupBy, indexBy, countBy, toArray, size, partition, first, head, take, initial, last, rest, tail, drop, compact, flatten, without, uniq, unique, union, intersection, difference, unzip, zip, object, findIndex, findLastIndex, sortedIndex, indexOf, lastIndexOf, range, chunk, bind, partial, bindAll, memoize, delay, defer, throttle, debounce, wrap, negate, compose, after, before, once, keys, allKeys, values, mapObject, pairs, invert, functions, methods, extend, extendOwn, assign, findKey, pick, omit, defaults, create, clone, tap, isMatch, isEqual, isEmpty, isElement, isArray, isObject, isArguments, isFunction, isString, isNumber, isDate, isRegExp, isError, isSymbol, isMap, isWeakMap, isSet, isWeakSet, isFinite, isNaN, isBoolean, isNull, isUndefined, has, identity, constant, noop, property, propertyOf, matcher, matches, times, random, now, escape, unescape, result, uniqueId, templateSettings, template, chain, mixin */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function(global) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return _; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "VERSION", function() { return VERSION; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "iteratee", function() { return iteratee; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "restArguments", function() { return restArguments; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "each", function() { return each; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "forEach", function() { return each; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "map", function() { return map; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "collect", function() { return map; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "reduce", function() { return reduce; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "foldl", function() { return reduce; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "inject", function() { return reduce; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "reduceRight", function() { return reduceRight; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "foldr", function() { return reduceRight; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "find", function() { return find; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "detect", function() { return find; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "filter", function() { return filter; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "select", function() { return filter; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "reject", function() { return reject; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "every", function() { return every; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "all", function() { return every; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "some", function() { return some; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "any", function() { return some; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "contains", function() { return contains; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "includes", function() { return contains; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "include", function() { return contains; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "invoke", function() { return invoke; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "pluck", function() { return pluck; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "where", function() { return where; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findWhere", function() { return findWhere; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "max", function() { return max; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "min", function() { return min; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "shuffle", function() { return shuffle; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sample", function() { return sample; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sortBy", function() { return sortBy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "groupBy", function() { return groupBy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "indexBy", function() { return indexBy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "countBy", function() { return countBy; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "toArray", function() { return toArray; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "size", function() { return size; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "partition", function() { return partition; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "first", function() { return first; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "head", function() { return first; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "take", function() { return first; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "initial", function() { return initial; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "last", function() { return last; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "rest", function() { return rest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "tail", function() { return rest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "drop", function() { return rest; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "compact", function() { return compact; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "flatten", function() { return flatten; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "without", function() { return without; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "uniq", function() { return uniq; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "unique", function() { return uniq; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "union", function() { return union; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "intersection", function() { return intersection; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "difference", function() { return difference; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "unzip", function() { return unzip; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "zip", function() { return zip; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "object", function() { return object; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findIndex", function() { return findIndex; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findLastIndex", function() { return findLastIndex; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sortedIndex", function() { return sortedIndex; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "indexOf", function() { return indexOf; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "lastIndexOf", function() { return lastIndexOf; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "range", function() { return range; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "chunk", function() { return chunk; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "bind", function() { return bind; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "partial", function() { return partial; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "bindAll", function() { return bindAll; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "memoize", function() { return memoize; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "delay", function() { return delay; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "defer", function() { return defer; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "throttle", function() { return throttle; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "debounce", function() { return debounce; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "wrap", function() { return wrap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "negate", function() { return negate; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "compose", function() { return compose; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "after", function() { return after; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "before", function() { return before; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "once", function() { return once; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "keys", function() { return keys; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "allKeys", function() { return allKeys; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "values", function() { return values; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mapObject", function() { return mapObject; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "pairs", function() { return pairs; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "invert", function() { return invert; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "functions", function() { return functions; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "methods", function() { return functions; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "extend", function() { return extend; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "extendOwn", function() { return extendOwn; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "assign", function() { return extendOwn; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "findKey", function() { return findKey; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "pick", function() { return pick; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "omit", function() { return omit; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "defaults", function() { return defaults; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "create", function() { return create; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "clone", function() { return clone; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "tap", function() { return tap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isMatch", function() { return isMatch; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isEqual", function() { return isEqual; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isEmpty", function() { return isEmpty; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isElement", function() { return isElement; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isArray", function() { return isArray; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isObject", function() { return isObject; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isArguments", function() { return isArguments; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isFunction", function() { return isFunction; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isString", function() { return isString; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isNumber", function() { return isNumber; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isDate", function() { return isDate; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isRegExp", function() { return isRegExp; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isError", function() { return isError; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isSymbol", function() { return isSymbol; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isMap", function() { return isMap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isWeakMap", function() { return isWeakMap; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isSet", function() { return isSet; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isWeakSet", function() { return isWeakSet; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isFinite", function() { return isFinite; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isNaN", function() { return isNaN; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isBoolean", function() { return isBoolean; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isNull", function() { return isNull; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "isUndefined", function() { return isUndefined; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "has", function() { return has; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "identity", function() { return identity; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "constant", function() { return constant; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "noop", function() { return noop; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "property", function() { return property; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "propertyOf", function() { return propertyOf; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "matcher", function() { return matcher; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "matches", function() { return matcher; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "times", function() { return times; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "random", function() { return random; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "now", function() { return now; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "escape", function() { return escape; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "unescape", function() { return unescape; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "result", function() { return result; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "uniqueId", function() { return uniqueId; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "templateSettings", function() { return templateSettings; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "template", function() { return template; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "chain", function() { return chain; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mixin", function() { return mixin; });
//     Underscore.js 1.10.2
//     https://underscorejs.org
//     (c) 2009-2020 Jeremy Ashkenas, DocumentCloud and Investigative Reporters & Editors
//     Underscore may be freely distributed under the MIT license.

// Baseline setup
// --------------

// Establish the root object, `window` (`self`) in the browser, `global`
// on the server, or `this` in some virtual machines. We use `self`
// instead of `window` for `WebWorker` support.
var root = typeof self == 'object' && self.self === self && self ||
          typeof global == 'object' && global.global === global && global ||
          Function('return this')() ||
          {};

// Save bytes in the minified (but not gzipped) version:
var ArrayProto = Array.prototype, ObjProto = Object.prototype;
var SymbolProto = typeof Symbol !== 'undefined' ? Symbol.prototype : null;

// Create quick reference variables for speed access to core prototypes.
var push = ArrayProto.push,
    slice = ArrayProto.slice,
    toString = ObjProto.toString,
    hasOwnProperty = ObjProto.hasOwnProperty;

// All **ECMAScript 5** native function implementations that we hope to use
// are declared here.
var nativeIsArray = Array.isArray,
    nativeKeys = Object.keys,
    nativeCreate = Object.create;

// Create references to these builtin functions because we override them.
var _isNaN = root.isNaN,
    _isFinite = root.isFinite;

// Naked function reference for surrogate-prototype-swapping.
var Ctor = function(){};

// The Underscore object. All exported functions below are added to it in the
// modules/index-all.js using the mixin function.
function _(obj) {
  if (obj instanceof _) return obj;
  if (!(this instanceof _)) return new _(obj);
  this._wrapped = obj;
}

// Current version.
var VERSION = _.VERSION = '1.10.2';

// Internal function that returns an efficient (for current engines) version
// of the passed-in callback, to be repeatedly applied in other Underscore
// functions.
function optimizeCb(func, context, argCount) {
  if (context === void 0) return func;
  switch (argCount == null ? 3 : argCount) {
    case 1: return function(value) {
      return func.call(context, value);
    };
    // The 2-argument case is omitted because we’re not using it.
    case 3: return function(value, index, collection) {
      return func.call(context, value, index, collection);
    };
    case 4: return function(accumulator, value, index, collection) {
      return func.call(context, accumulator, value, index, collection);
    };
  }
  return function() {
    return func.apply(context, arguments);
  };
}

// An internal function to generate callbacks that can be applied to each
// element in a collection, returning the desired result — either `identity`,
// an arbitrary callback, a property matcher, or a property accessor.
function baseIteratee(value, context, argCount) {
  if (value == null) return identity;
  if (isFunction(value)) return optimizeCb(value, context, argCount);
  if (isObject(value) && !isArray(value)) return matcher(value);
  return property(value);
}

// External wrapper for our callback generator. Users may customize
// `_.iteratee` if they want additional predicate/iteratee shorthand styles.
// This abstraction hides the internal-only argCount argument.
_.iteratee = iteratee;
function iteratee(value, context) {
  return baseIteratee(value, context, Infinity);
}

// The function we actually call internally. It invokes _.iteratee if
// overridden, otherwise baseIteratee.
function cb(value, context, argCount) {
  if (_.iteratee !== iteratee) return _.iteratee(value, context);
  return baseIteratee(value, context, argCount);
}

// Some functions take a variable number of arguments, or a few expected
// arguments at the beginning and then a variable number of values to operate
// on. This helper accumulates all remaining arguments past the function’s
// argument length (or an explicit `startIndex`), into an array that becomes
// the last argument. Similar to ES6’s "rest parameter".
function restArguments(func, startIndex) {
  startIndex = startIndex == null ? func.length - 1 : +startIndex;
  return function() {
    var length = Math.max(arguments.length - startIndex, 0),
        rest = Array(length),
        index = 0;
    for (; index < length; index++) {
      rest[index] = arguments[index + startIndex];
    }
    switch (startIndex) {
      case 0: return func.call(this, rest);
      case 1: return func.call(this, arguments[0], rest);
      case 2: return func.call(this, arguments[0], arguments[1], rest);
    }
    var args = Array(startIndex + 1);
    for (index = 0; index < startIndex; index++) {
      args[index] = arguments[index];
    }
    args[startIndex] = rest;
    return func.apply(this, args);
  };
}

// An internal function for creating a new object that inherits from another.
function baseCreate(prototype) {
  if (!isObject(prototype)) return {};
  if (nativeCreate) return nativeCreate(prototype);
  Ctor.prototype = prototype;
  var result = new Ctor;
  Ctor.prototype = null;
  return result;
}

function shallowProperty(key) {
  return function(obj) {
    return obj == null ? void 0 : obj[key];
  };
}

function _has(obj, path) {
  return obj != null && hasOwnProperty.call(obj, path);
}

function deepGet(obj, path) {
  var length = path.length;
  for (var i = 0; i < length; i++) {
    if (obj == null) return void 0;
    obj = obj[path[i]];
  }
  return length ? obj : void 0;
}

// Helper for collection methods to determine whether a collection
// should be iterated as an array or as an object.
// Related: https://people.mozilla.org/~jorendorff/es6-draft.html#sec-tolength
// Avoids a very nasty iOS 8 JIT bug on ARM-64. #2094
var MAX_ARRAY_INDEX = Math.pow(2, 53) - 1;
var getLength = shallowProperty('length');
function isArrayLike(collection) {
  var length = getLength(collection);
  return typeof length == 'number' && length >= 0 && length <= MAX_ARRAY_INDEX;
}

// Collection Functions
// --------------------

// The cornerstone, an `each` implementation, aka `forEach`.
// Handles raw objects in addition to array-likes. Treats all
// sparse array-likes as if they were dense.
function each(obj, iteratee, context) {
  iteratee = optimizeCb(iteratee, context);
  var i, length;
  if (isArrayLike(obj)) {
    for (i = 0, length = obj.length; i < length; i++) {
      iteratee(obj[i], i, obj);
    }
  } else {
    var _keys = keys(obj);
    for (i = 0, length = _keys.length; i < length; i++) {
      iteratee(obj[_keys[i]], _keys[i], obj);
    }
  }
  return obj;
}


// Return the results of applying the iteratee to each element.
function map(obj, iteratee, context) {
  iteratee = cb(iteratee, context);
  var _keys = !isArrayLike(obj) && keys(obj),
      length = (_keys || obj).length,
      results = Array(length);
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    results[index] = iteratee(obj[currentKey], currentKey, obj);
  }
  return results;
}


// Create a reducing function iterating left or right.
function createReduce(dir) {
  // Wrap code that reassigns argument variables in a separate function than
  // the one that accesses `arguments.length` to avoid a perf hit. (#1991)
  var reducer = function(obj, iteratee, memo, initial) {
    var _keys = !isArrayLike(obj) && keys(obj),
        length = (_keys || obj).length,
        index = dir > 0 ? 0 : length - 1;
    if (!initial) {
      memo = obj[_keys ? _keys[index] : index];
      index += dir;
    }
    for (; index >= 0 && index < length; index += dir) {
      var currentKey = _keys ? _keys[index] : index;
      memo = iteratee(memo, obj[currentKey], currentKey, obj);
    }
    return memo;
  };

  return function(obj, iteratee, memo, context) {
    var initial = arguments.length >= 3;
    return reducer(obj, optimizeCb(iteratee, context, 4), memo, initial);
  };
}

// **Reduce** builds up a single result from a list of values, aka `inject`,
// or `foldl`.
var reduce = createReduce(1);


// The right-associative version of reduce, also known as `foldr`.
var reduceRight = createReduce(-1);


// Return the first value which passes a truth test.
function find(obj, predicate, context) {
  var keyFinder = isArrayLike(obj) ? findIndex : findKey;
  var key = keyFinder(obj, predicate, context);
  if (key !== void 0 && key !== -1) return obj[key];
}


// Return all the elements that pass a truth test.
function filter(obj, predicate, context) {
  var results = [];
  predicate = cb(predicate, context);
  each(obj, function(value, index, list) {
    if (predicate(value, index, list)) results.push(value);
  });
  return results;
}


// Return all the elements for which a truth test fails.
function reject(obj, predicate, context) {
  return filter(obj, negate(cb(predicate)), context);
}

// Determine whether all of the elements match a truth test.
function every(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = !isArrayLike(obj) && keys(obj),
      length = (_keys || obj).length;
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    if (!predicate(obj[currentKey], currentKey, obj)) return false;
  }
  return true;
}


// Determine if at least one element in the object matches a truth test.
function some(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = !isArrayLike(obj) && keys(obj),
      length = (_keys || obj).length;
  for (var index = 0; index < length; index++) {
    var currentKey = _keys ? _keys[index] : index;
    if (predicate(obj[currentKey], currentKey, obj)) return true;
  }
  return false;
}


// Determine if the array or object contains a given item (using `===`).
function contains(obj, item, fromIndex, guard) {
  if (!isArrayLike(obj)) obj = values(obj);
  if (typeof fromIndex != 'number' || guard) fromIndex = 0;
  return indexOf(obj, item, fromIndex) >= 0;
}


// Invoke a method (with arguments) on every item in a collection.
var invoke = restArguments(function(obj, path, args) {
  var contextPath, func;
  if (isFunction(path)) {
    func = path;
  } else if (isArray(path)) {
    contextPath = path.slice(0, -1);
    path = path[path.length - 1];
  }
  return map(obj, function(context) {
    var method = func;
    if (!method) {
      if (contextPath && contextPath.length) {
        context = deepGet(context, contextPath);
      }
      if (context == null) return void 0;
      method = context[path];
    }
    return method == null ? method : method.apply(context, args);
  });
});

// Convenience version of a common use case of `map`: fetching a property.
function pluck(obj, key) {
  return map(obj, property(key));
}

// Convenience version of a common use case of `filter`: selecting only objects
// containing specific `key:value` pairs.
function where(obj, attrs) {
  return filter(obj, matcher(attrs));
}

// Convenience version of a common use case of `find`: getting the first object
// containing specific `key:value` pairs.
function findWhere(obj, attrs) {
  return find(obj, matcher(attrs));
}

// Return the maximum element (or element-based computation).
function max(obj, iteratee, context) {
  var result = -Infinity, lastComputed = -Infinity,
      value, computed;
  if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
    obj = isArrayLike(obj) ? obj : values(obj);
    for (var i = 0, length = obj.length; i < length; i++) {
      value = obj[i];
      if (value != null && value > result) {
        result = value;
      }
    }
  } else {
    iteratee = cb(iteratee, context);
    each(obj, function(v, index, list) {
      computed = iteratee(v, index, list);
      if (computed > lastComputed || computed === -Infinity && result === -Infinity) {
        result = v;
        lastComputed = computed;
      }
    });
  }
  return result;
}

// Return the minimum element (or element-based computation).
function min(obj, iteratee, context) {
  var result = Infinity, lastComputed = Infinity,
      value, computed;
  if (iteratee == null || typeof iteratee == 'number' && typeof obj[0] != 'object' && obj != null) {
    obj = isArrayLike(obj) ? obj : values(obj);
    for (var i = 0, length = obj.length; i < length; i++) {
      value = obj[i];
      if (value != null && value < result) {
        result = value;
      }
    }
  } else {
    iteratee = cb(iteratee, context);
    each(obj, function(v, index, list) {
      computed = iteratee(v, index, list);
      if (computed < lastComputed || computed === Infinity && result === Infinity) {
        result = v;
        lastComputed = computed;
      }
    });
  }
  return result;
}

// Shuffle a collection.
function shuffle(obj) {
  return sample(obj, Infinity);
}

// Sample **n** random values from a collection using the modern version of the
// [Fisher-Yates shuffle](https://en.wikipedia.org/wiki/Fisher–Yates_shuffle).
// If **n** is not specified, returns a single random element.
// The internal `guard` argument allows it to work with `map`.
function sample(obj, n, guard) {
  if (n == null || guard) {
    if (!isArrayLike(obj)) obj = values(obj);
    return obj[random(obj.length - 1)];
  }
  var sample = isArrayLike(obj) ? clone(obj) : values(obj);
  var length = getLength(sample);
  n = Math.max(Math.min(n, length), 0);
  var last = length - 1;
  for (var index = 0; index < n; index++) {
    var rand = random(index, last);
    var temp = sample[index];
    sample[index] = sample[rand];
    sample[rand] = temp;
  }
  return sample.slice(0, n);
}

// Sort the object's values by a criterion produced by an iteratee.
function sortBy(obj, iteratee, context) {
  var index = 0;
  iteratee = cb(iteratee, context);
  return pluck(map(obj, function(value, key, list) {
    return {
      value: value,
      index: index++,
      criteria: iteratee(value, key, list)
    };
  }).sort(function(left, right) {
    var a = left.criteria;
    var b = right.criteria;
    if (a !== b) {
      if (a > b || a === void 0) return 1;
      if (a < b || b === void 0) return -1;
    }
    return left.index - right.index;
  }), 'value');
}

// An internal function used for aggregate "group by" operations.
function group(behavior, partition) {
  return function(obj, iteratee, context) {
    var result = partition ? [[], []] : {};
    iteratee = cb(iteratee, context);
    each(obj, function(value, index) {
      var key = iteratee(value, index, obj);
      behavior(result, value, key);
    });
    return result;
  };
}

// Groups the object's values by a criterion. Pass either a string attribute
// to group by, or a function that returns the criterion.
var groupBy = group(function(result, value, key) {
  if (_has(result, key)) result[key].push(value); else result[key] = [value];
});

// Indexes the object's values by a criterion, similar to `groupBy`, but for
// when you know that your index values will be unique.
var indexBy = group(function(result, value, key) {
  result[key] = value;
});

// Counts instances of an object that group by a certain criterion. Pass
// either a string attribute to count by, or a function that returns the
// criterion.
var countBy = group(function(result, value, key) {
  if (_has(result, key)) result[key]++; else result[key] = 1;
});

var reStrSymbol = /[^\ud800-\udfff]|[\ud800-\udbff][\udc00-\udfff]|[\ud800-\udfff]/g;
// Safely create a real, live array from anything iterable.
function toArray(obj) {
  if (!obj) return [];
  if (isArray(obj)) return slice.call(obj);
  if (isString(obj)) {
    // Keep surrogate pair characters together
    return obj.match(reStrSymbol);
  }
  if (isArrayLike(obj)) return map(obj, identity);
  return values(obj);
}

// Return the number of elements in an object.
function size(obj) {
  if (obj == null) return 0;
  return isArrayLike(obj) ? obj.length : keys(obj).length;
}

// Split a collection into two arrays: one whose elements all satisfy the given
// predicate, and one whose elements all do not satisfy the predicate.
var partition = group(function(result, value, pass) {
  result[pass ? 0 : 1].push(value);
}, true);

// Array Functions
// ---------------

// Get the first element of an array. Passing **n** will return the first N
// values in the array. The **guard** check allows it to work with `map`.
function first(array, n, guard) {
  if (array == null || array.length < 1) return n == null ? void 0 : [];
  if (n == null || guard) return array[0];
  return initial(array, array.length - n);
}


// Returns everything but the last entry of the array. Especially useful on
// the arguments object. Passing **n** will return all the values in
// the array, excluding the last N.
function initial(array, n, guard) {
  return slice.call(array, 0, Math.max(0, array.length - (n == null || guard ? 1 : n)));
}

// Get the last element of an array. Passing **n** will return the last N
// values in the array.
function last(array, n, guard) {
  if (array == null || array.length < 1) return n == null ? void 0 : [];
  if (n == null || guard) return array[array.length - 1];
  return rest(array, Math.max(0, array.length - n));
}

// Returns everything but the first entry of the array. Especially useful on
// the arguments object. Passing an **n** will return the rest N values in the
// array.
function rest(array, n, guard) {
  return slice.call(array, n == null || guard ? 1 : n);
}


// Trim out all falsy values from an array.
function compact(array) {
  return filter(array, Boolean);
}

// Internal implementation of a recursive `flatten` function.
function _flatten(input, shallow, strict, output) {
  output = output || [];
  var idx = output.length;
  for (var i = 0, length = getLength(input); i < length; i++) {
    var value = input[i];
    if (isArrayLike(value) && (isArray(value) || isArguments(value))) {
      // Flatten current level of array or arguments object.
      if (shallow) {
        var j = 0, len = value.length;
        while (j < len) output[idx++] = value[j++];
      } else {
        _flatten(value, shallow, strict, output);
        idx = output.length;
      }
    } else if (!strict) {
      output[idx++] = value;
    }
  }
  return output;
}

// Flatten out an array, either recursively (by default), or just one level.
function flatten(array, shallow) {
  return _flatten(array, shallow, false);
}

// Return a version of the array that does not contain the specified value(s).
var without = restArguments(function(array, otherArrays) {
  return difference(array, otherArrays);
});

// Produce a duplicate-free version of the array. If the array has already
// been sorted, you have the option of using a faster algorithm.
// The faster algorithm will not work with an iteratee if the iteratee
// is not a one-to-one function, so providing an iteratee will disable
// the faster algorithm.
function uniq(array, isSorted, iteratee, context) {
  if (!isBoolean(isSorted)) {
    context = iteratee;
    iteratee = isSorted;
    isSorted = false;
  }
  if (iteratee != null) iteratee = cb(iteratee, context);
  var result = [];
  var seen = [];
  for (var i = 0, length = getLength(array); i < length; i++) {
    var value = array[i],
        computed = iteratee ? iteratee(value, i, array) : value;
    if (isSorted && !iteratee) {
      if (!i || seen !== computed) result.push(value);
      seen = computed;
    } else if (iteratee) {
      if (!contains(seen, computed)) {
        seen.push(computed);
        result.push(value);
      }
    } else if (!contains(result, value)) {
      result.push(value);
    }
  }
  return result;
}


// Produce an array that contains the union: each distinct element from all of
// the passed-in arrays.
var union = restArguments(function(arrays) {
  return uniq(_flatten(arrays, true, true));
});

// Produce an array that contains every item shared between all the
// passed-in arrays.
function intersection(array) {
  var result = [];
  var argsLength = arguments.length;
  for (var i = 0, length = getLength(array); i < length; i++) {
    var item = array[i];
    if (contains(result, item)) continue;
    var j;
    for (j = 1; j < argsLength; j++) {
      if (!contains(arguments[j], item)) break;
    }
    if (j === argsLength) result.push(item);
  }
  return result;
}

// Take the difference between one array and a number of other arrays.
// Only the elements present in just the first array will remain.
var difference = restArguments(function(array, rest) {
  rest = _flatten(rest, true, true);
  return filter(array, function(value){
    return !contains(rest, value);
  });
});

// Complement of zip. Unzip accepts an array of arrays and groups
// each array's elements on shared indices.
function unzip(array) {
  var length = array && max(array, getLength).length || 0;
  var result = Array(length);

  for (var index = 0; index < length; index++) {
    result[index] = pluck(array, index);
  }
  return result;
}

// Zip together multiple lists into a single array -- elements that share
// an index go together.
var zip = restArguments(unzip);

// Converts lists into objects. Pass either a single array of `[key, value]`
// pairs, or two parallel arrays of the same length -- one of keys, and one of
// the corresponding values. Passing by pairs is the reverse of pairs.
function object(list, values) {
  var result = {};
  for (var i = 0, length = getLength(list); i < length; i++) {
    if (values) {
      result[list[i]] = values[i];
    } else {
      result[list[i][0]] = list[i][1];
    }
  }
  return result;
}

// Generator function to create the findIndex and findLastIndex functions.
function createPredicateIndexFinder(dir) {
  return function(array, predicate, context) {
    predicate = cb(predicate, context);
    var length = getLength(array);
    var index = dir > 0 ? 0 : length - 1;
    for (; index >= 0 && index < length; index += dir) {
      if (predicate(array[index], index, array)) return index;
    }
    return -1;
  };
}

// Returns the first index on an array-like that passes a predicate test.
var findIndex = createPredicateIndexFinder(1);
var findLastIndex = createPredicateIndexFinder(-1);

// Use a comparator function to figure out the smallest index at which
// an object should be inserted so as to maintain order. Uses binary search.
function sortedIndex(array, obj, iteratee, context) {
  iteratee = cb(iteratee, context, 1);
  var value = iteratee(obj);
  var low = 0, high = getLength(array);
  while (low < high) {
    var mid = Math.floor((low + high) / 2);
    if (iteratee(array[mid]) < value) low = mid + 1; else high = mid;
  }
  return low;
}

// Generator function to create the indexOf and lastIndexOf functions.
function createIndexFinder(dir, predicateFind, sortedIndex) {
  return function(array, item, idx) {
    var i = 0, length = getLength(array);
    if (typeof idx == 'number') {
      if (dir > 0) {
        i = idx >= 0 ? idx : Math.max(idx + length, i);
      } else {
        length = idx >= 0 ? Math.min(idx + 1, length) : idx + length + 1;
      }
    } else if (sortedIndex && idx && length) {
      idx = sortedIndex(array, item);
      return array[idx] === item ? idx : -1;
    }
    if (item !== item) {
      idx = predicateFind(slice.call(array, i, length), isNaN);
      return idx >= 0 ? idx + i : -1;
    }
    for (idx = dir > 0 ? i : length - 1; idx >= 0 && idx < length; idx += dir) {
      if (array[idx] === item) return idx;
    }
    return -1;
  };
}

// Return the position of the first occurrence of an item in an array,
// or -1 if the item is not included in the array.
// If the array is large and already in sort order, pass `true`
// for **isSorted** to use binary search.
var indexOf = createIndexFinder(1, findIndex, sortedIndex);
var lastIndexOf = createIndexFinder(-1, findLastIndex);

// Generate an integer Array containing an arithmetic progression. A port of
// the native Python `range()` function. See
// [the Python documentation](https://docs.python.org/library/functions.html#range).
function range(start, stop, step) {
  if (stop == null) {
    stop = start || 0;
    start = 0;
  }
  if (!step) {
    step = stop < start ? -1 : 1;
  }

  var length = Math.max(Math.ceil((stop - start) / step), 0);
  var range = Array(length);

  for (var idx = 0; idx < length; idx++, start += step) {
    range[idx] = start;
  }

  return range;
}

// Chunk a single array into multiple arrays, each containing `count` or fewer
// items.
function chunk(array, count) {
  if (count == null || count < 1) return [];
  var result = [];
  var i = 0, length = array.length;
  while (i < length) {
    result.push(slice.call(array, i, i += count));
  }
  return result;
}

// Function (ahem) Functions
// ------------------

// Determines whether to execute a function as a constructor
// or a normal function with the provided arguments.
function executeBound(sourceFunc, boundFunc, context, callingContext, args) {
  if (!(callingContext instanceof boundFunc)) return sourceFunc.apply(context, args);
  var self = baseCreate(sourceFunc.prototype);
  var result = sourceFunc.apply(self, args);
  if (isObject(result)) return result;
  return self;
}

// Create a function bound to a given object (assigning `this`, and arguments,
// optionally). Delegates to **ECMAScript 5**'s native `Function.bind` if
// available.
var bind = restArguments(function(func, context, args) {
  if (!isFunction(func)) throw new TypeError('Bind must be called on a function');
  var bound = restArguments(function(callArgs) {
    return executeBound(func, bound, context, this, args.concat(callArgs));
  });
  return bound;
});

// Partially apply a function by creating a version that has had some of its
// arguments pre-filled, without changing its dynamic `this` context. _ acts
// as a placeholder by default, allowing any combination of arguments to be
// pre-filled. Set `partial.placeholder` for a custom placeholder argument.
var partial = restArguments(function(func, boundArgs) {
  var placeholder = partial.placeholder;
  var bound = function() {
    var position = 0, length = boundArgs.length;
    var args = Array(length);
    for (var i = 0; i < length; i++) {
      args[i] = boundArgs[i] === placeholder ? arguments[position++] : boundArgs[i];
    }
    while (position < arguments.length) args.push(arguments[position++]);
    return executeBound(func, bound, this, this, args);
  };
  return bound;
});

partial.placeholder = _;

// Bind a number of an object's methods to that object. Remaining arguments
// are the method names to be bound. Useful for ensuring that all callbacks
// defined on an object belong to it.
var bindAll = restArguments(function(obj, _keys) {
  _keys = _flatten(_keys, false, false);
  var index = _keys.length;
  if (index < 1) throw new Error('bindAll must be passed function names');
  while (index--) {
    var key = _keys[index];
    obj[key] = bind(obj[key], obj);
  }
});

// Memoize an expensive function by storing its results.
function memoize(func, hasher) {
  var memoize = function(key) {
    var cache = memoize.cache;
    var address = '' + (hasher ? hasher.apply(this, arguments) : key);
    if (!_has(cache, address)) cache[address] = func.apply(this, arguments);
    return cache[address];
  };
  memoize.cache = {};
  return memoize;
}

// Delays a function for the given number of milliseconds, and then calls
// it with the arguments supplied.
var delay = restArguments(function(func, wait, args) {
  return setTimeout(function() {
    return func.apply(null, args);
  }, wait);
});

// Defers a function, scheduling it to run after the current call stack has
// cleared.
var defer = partial(delay, _, 1);

// Returns a function, that, when invoked, will only be triggered at most once
// during a given window of time. Normally, the throttled function will run
// as much as it can, without ever going more than once per `wait` duration;
// but if you'd like to disable the execution on the leading edge, pass
// `{leading: false}`. To disable execution on the trailing edge, ditto.
function throttle(func, wait, options) {
  var timeout, context, args, result;
  var previous = 0;
  if (!options) options = {};

  var later = function() {
    previous = options.leading === false ? 0 : now();
    timeout = null;
    result = func.apply(context, args);
    if (!timeout) context = args = null;
  };

  var throttled = function() {
    var _now = now();
    if (!previous && options.leading === false) previous = _now;
    var remaining = wait - (_now - previous);
    context = this;
    args = arguments;
    if (remaining <= 0 || remaining > wait) {
      if (timeout) {
        clearTimeout(timeout);
        timeout = null;
      }
      previous = _now;
      result = func.apply(context, args);
      if (!timeout) context = args = null;
    } else if (!timeout && options.trailing !== false) {
      timeout = setTimeout(later, remaining);
    }
    return result;
  };

  throttled.cancel = function() {
    clearTimeout(timeout);
    previous = 0;
    timeout = context = args = null;
  };

  return throttled;
}

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce(func, wait, immediate) {
  var timeout, result;

  var later = function(context, args) {
    timeout = null;
    if (args) result = func.apply(context, args);
  };

  var debounced = restArguments(function(args) {
    if (timeout) clearTimeout(timeout);
    if (immediate) {
      var callNow = !timeout;
      timeout = setTimeout(later, wait);
      if (callNow) result = func.apply(this, args);
    } else {
      timeout = delay(later, wait, this, args);
    }

    return result;
  });

  debounced.cancel = function() {
    clearTimeout(timeout);
    timeout = null;
  };

  return debounced;
}

// Returns the first function passed as an argument to the second,
// allowing you to adjust arguments, run code before and after, and
// conditionally execute the original function.
function wrap(func, wrapper) {
  return partial(wrapper, func);
}

// Returns a negated version of the passed-in predicate.
function negate(predicate) {
  return function() {
    return !predicate.apply(this, arguments);
  };
}

// Returns a function that is the composition of a list of functions, each
// consuming the return value of the function that follows.
function compose() {
  var args = arguments;
  var start = args.length - 1;
  return function() {
    var i = start;
    var result = args[start].apply(this, arguments);
    while (i--) result = args[i].call(this, result);
    return result;
  };
}

// Returns a function that will only be executed on and after the Nth call.
function after(times, func) {
  return function() {
    if (--times < 1) {
      return func.apply(this, arguments);
    }
  };
}

// Returns a function that will only be executed up to (but not including) the Nth call.
function before(times, func) {
  var memo;
  return function() {
    if (--times > 0) {
      memo = func.apply(this, arguments);
    }
    if (times <= 1) func = null;
    return memo;
  };
}

// Returns a function that will be executed at most one time, no matter how
// often you call it. Useful for lazy initialization.
var once = partial(before, 2);

// Object Functions
// ----------------

// Keys in IE < 9 that won't be iterated by `for key in ...` and thus missed.
var hasEnumBug = !{toString: null}.propertyIsEnumerable('toString');
var nonEnumerableProps = ['valueOf', 'isPrototypeOf', 'toString',
  'propertyIsEnumerable', 'hasOwnProperty', 'toLocaleString'];

function collectNonEnumProps(obj, _keys) {
  var nonEnumIdx = nonEnumerableProps.length;
  var constructor = obj.constructor;
  var proto = isFunction(constructor) && constructor.prototype || ObjProto;

  // Constructor is a special case.
  var prop = 'constructor';
  if (_has(obj, prop) && !contains(_keys, prop)) _keys.push(prop);

  while (nonEnumIdx--) {
    prop = nonEnumerableProps[nonEnumIdx];
    if (prop in obj && obj[prop] !== proto[prop] && !contains(_keys, prop)) {
      _keys.push(prop);
    }
  }
}

// Retrieve the names of an object's own properties.
// Delegates to **ECMAScript 5**'s native `Object.keys`.
function keys(obj) {
  if (!isObject(obj)) return [];
  if (nativeKeys) return nativeKeys(obj);
  var _keys = [];
  for (var key in obj) if (_has(obj, key)) _keys.push(key);
  // Ahem, IE < 9.
  if (hasEnumBug) collectNonEnumProps(obj, _keys);
  return _keys;
}

// Retrieve all the property names of an object.
function allKeys(obj) {
  if (!isObject(obj)) return [];
  var _keys = [];
  for (var key in obj) _keys.push(key);
  // Ahem, IE < 9.
  if (hasEnumBug) collectNonEnumProps(obj, _keys);
  return _keys;
}

// Retrieve the values of an object's properties.
function values(obj) {
  var _keys = keys(obj);
  var length = _keys.length;
  var values = Array(length);
  for (var i = 0; i < length; i++) {
    values[i] = obj[_keys[i]];
  }
  return values;
}

// Returns the results of applying the iteratee to each element of the object.
// In contrast to map it returns an object.
function mapObject(obj, iteratee, context) {
  iteratee = cb(iteratee, context);
  var _keys = keys(obj),
      length = _keys.length,
      results = {};
  for (var index = 0; index < length; index++) {
    var currentKey = _keys[index];
    results[currentKey] = iteratee(obj[currentKey], currentKey, obj);
  }
  return results;
}

// Convert an object into a list of `[key, value]` pairs.
// The opposite of object.
function pairs(obj) {
  var _keys = keys(obj);
  var length = _keys.length;
  var pairs = Array(length);
  for (var i = 0; i < length; i++) {
    pairs[i] = [_keys[i], obj[_keys[i]]];
  }
  return pairs;
}

// Invert the keys and values of an object. The values must be serializable.
function invert(obj) {
  var result = {};
  var _keys = keys(obj);
  for (var i = 0, length = _keys.length; i < length; i++) {
    result[obj[_keys[i]]] = _keys[i];
  }
  return result;
}

// Return a sorted list of the function names available on the object.
function functions(obj) {
  var names = [];
  for (var key in obj) {
    if (isFunction(obj[key])) names.push(key);
  }
  return names.sort();
}


// An internal function for creating assigner functions.
function createAssigner(keysFunc, defaults) {
  return function(obj) {
    var length = arguments.length;
    if (defaults) obj = Object(obj);
    if (length < 2 || obj == null) return obj;
    for (var index = 1; index < length; index++) {
      var source = arguments[index],
          _keys = keysFunc(source),
          l = _keys.length;
      for (var i = 0; i < l; i++) {
        var key = _keys[i];
        if (!defaults || obj[key] === void 0) obj[key] = source[key];
      }
    }
    return obj;
  };
}

// Extend a given object with all the properties in passed-in object(s).
var extend = createAssigner(allKeys);

// Assigns a given object with all the own properties in the passed-in object(s).
// (https://developer.mozilla.org/docs/Web/JavaScript/Reference/Global_Objects/Object/assign)
var extendOwn = createAssigner(keys);


// Returns the first key on an object that passes a predicate test.
function findKey(obj, predicate, context) {
  predicate = cb(predicate, context);
  var _keys = keys(obj), key;
  for (var i = 0, length = _keys.length; i < length; i++) {
    key = _keys[i];
    if (predicate(obj[key], key, obj)) return key;
  }
}

// Internal pick helper function to determine if `obj` has key `key`.
function keyInObj(value, key, obj) {
  return key in obj;
}

// Return a copy of the object only containing the whitelisted properties.
var pick = restArguments(function(obj, _keys) {
  var result = {}, iteratee = _keys[0];
  if (obj == null) return result;
  if (isFunction(iteratee)) {
    if (_keys.length > 1) iteratee = optimizeCb(iteratee, _keys[1]);
    _keys = allKeys(obj);
  } else {
    iteratee = keyInObj;
    _keys = _flatten(_keys, false, false);
    obj = Object(obj);
  }
  for (var i = 0, length = _keys.length; i < length; i++) {
    var key = _keys[i];
    var value = obj[key];
    if (iteratee(value, key, obj)) result[key] = value;
  }
  return result;
});

// Return a copy of the object without the blacklisted properties.
var omit = restArguments(function(obj, _keys) {
  var iteratee = _keys[0], context;
  if (isFunction(iteratee)) {
    iteratee = negate(iteratee);
    if (_keys.length > 1) context = _keys[1];
  } else {
    _keys = map(_flatten(_keys, false, false), String);
    iteratee = function(value, key) {
      return !contains(_keys, key);
    };
  }
  return pick(obj, iteratee, context);
});

// Fill in a given object with default properties.
var defaults = createAssigner(allKeys, true);

// Creates an object that inherits from the given prototype object.
// If additional properties are provided then they will be added to the
// created object.
function create(prototype, props) {
  var result = baseCreate(prototype);
  if (props) extendOwn(result, props);
  return result;
}

// Create a (shallow-cloned) duplicate of an object.
function clone(obj) {
  if (!isObject(obj)) return obj;
  return isArray(obj) ? obj.slice() : extend({}, obj);
}

// Invokes interceptor with the obj, and then returns obj.
// The primary purpose of this method is to "tap into" a method chain, in
// order to perform operations on intermediate results within the chain.
function tap(obj, interceptor) {
  interceptor(obj);
  return obj;
}

// Returns whether an object has a given set of `key:value` pairs.
function isMatch(object, attrs) {
  var _keys = keys(attrs), length = _keys.length;
  if (object == null) return !length;
  var obj = Object(object);
  for (var i = 0; i < length; i++) {
    var key = _keys[i];
    if (attrs[key] !== obj[key] || !(key in obj)) return false;
  }
  return true;
}


// Internal recursive comparison function for `isEqual`.
function eq(a, b, aStack, bStack) {
  // Identical objects are equal. `0 === -0`, but they aren't identical.
  // See the [Harmony `egal` proposal](https://wiki.ecmascript.org/doku.php?id=harmony:egal).
  if (a === b) return a !== 0 || 1 / a === 1 / b;
  // `null` or `undefined` only equal to itself (strict comparison).
  if (a == null || b == null) return false;
  // `NaN`s are equivalent, but non-reflexive.
  if (a !== a) return b !== b;
  // Exhaust primitive checks
  var type = typeof a;
  if (type !== 'function' && type !== 'object' && typeof b != 'object') return false;
  return deepEq(a, b, aStack, bStack);
}

// Internal recursive comparison function for `isEqual`.
function deepEq(a, b, aStack, bStack) {
  // Unwrap any wrapped objects.
  if (a instanceof _) a = a._wrapped;
  if (b instanceof _) b = b._wrapped;
  // Compare `[[Class]]` names.
  var className = toString.call(a);
  if (className !== toString.call(b)) return false;
  switch (className) {
    // Strings, numbers, regular expressions, dates, and booleans are compared by value.
    case '[object RegExp]':
    // RegExps are coerced to strings for comparison (Note: '' + /a/i === '/a/i')
    case '[object String]':
      // Primitives and their corresponding object wrappers are equivalent; thus, `"5"` is
      // equivalent to `new String("5")`.
      return '' + a === '' + b;
    case '[object Number]':
      // `NaN`s are equivalent, but non-reflexive.
      // Object(NaN) is equivalent to NaN.
      if (+a !== +a) return +b !== +b;
      // An `egal` comparison is performed for other numeric values.
      return +a === 0 ? 1 / +a === 1 / b : +a === +b;
    case '[object Date]':
    case '[object Boolean]':
      // Coerce dates and booleans to numeric primitive values. Dates are compared by their
      // millisecond representations. Note that invalid dates with millisecond representations
      // of `NaN` are not equivalent.
      return +a === +b;
    case '[object Symbol]':
      return SymbolProto.valueOf.call(a) === SymbolProto.valueOf.call(b);
  }

  var areArrays = className === '[object Array]';
  if (!areArrays) {
    if (typeof a != 'object' || typeof b != 'object') return false;

    // Objects with different constructors are not equivalent, but `Object`s or `Array`s
    // from different frames are.
    var aCtor = a.constructor, bCtor = b.constructor;
    if (aCtor !== bCtor && !(isFunction(aCtor) && aCtor instanceof aCtor &&
                             isFunction(bCtor) && bCtor instanceof bCtor)
                        && ('constructor' in a && 'constructor' in b)) {
      return false;
    }
  }
  // Assume equality for cyclic structures. The algorithm for detecting cyclic
  // structures is adapted from ES 5.1 section 15.12.3, abstract operation `JO`.

  // Initializing stack of traversed objects.
  // It's done here since we only need them for objects and arrays comparison.
  aStack = aStack || [];
  bStack = bStack || [];
  var length = aStack.length;
  while (length--) {
    // Linear search. Performance is inversely proportional to the number of
    // unique nested structures.
    if (aStack[length] === a) return bStack[length] === b;
  }

  // Add the first object to the stack of traversed objects.
  aStack.push(a);
  bStack.push(b);

  // Recursively compare objects and arrays.
  if (areArrays) {
    // Compare array lengths to determine if a deep comparison is necessary.
    length = a.length;
    if (length !== b.length) return false;
    // Deep compare the contents, ignoring non-numeric properties.
    while (length--) {
      if (!eq(a[length], b[length], aStack, bStack)) return false;
    }
  } else {
    // Deep compare objects.
    var _keys = keys(a), key;
    length = _keys.length;
    // Ensure that both objects contain the same number of properties before comparing deep equality.
    if (keys(b).length !== length) return false;
    while (length--) {
      // Deep compare each member
      key = _keys[length];
      if (!(_has(b, key) && eq(a[key], b[key], aStack, bStack))) return false;
    }
  }
  // Remove the first object from the stack of traversed objects.
  aStack.pop();
  bStack.pop();
  return true;
}

// Perform a deep comparison to check if two objects are equal.
function isEqual(a, b) {
  return eq(a, b);
}

// Is a given array, string, or object empty?
// An "empty" object has no enumerable own-properties.
function isEmpty(obj) {
  if (obj == null) return true;
  if (isArrayLike(obj) && (isArray(obj) || isString(obj) || isArguments(obj))) return obj.length === 0;
  return keys(obj).length === 0;
}

// Is a given value a DOM element?
function isElement(obj) {
  return !!(obj && obj.nodeType === 1);
}

// Internal function for creating a toString-based type tester.
function tagTester(name) {
  return function(obj) {
    return toString.call(obj) === '[object ' + name + ']';
  };
}

// Is a given value an array?
// Delegates to ECMA5's native Array.isArray
var isArray = nativeIsArray || tagTester('Array');

// Is a given variable an object?
function isObject(obj) {
  var type = typeof obj;
  return type === 'function' || type === 'object' && !!obj;
}

// Add some isType methods: isArguments, isFunction, isString, isNumber, isDate, isRegExp, isError, isMap, isWeakMap, isSet, isWeakSet.
var isArguments = tagTester('Arguments');
var isFunction = tagTester('Function');
var isString = tagTester('String');
var isNumber = tagTester('Number');
var isDate = tagTester('Date');
var isRegExp = tagTester('RegExp');
var isError = tagTester('Error');
var isSymbol = tagTester('Symbol');
var isMap = tagTester('Map');
var isWeakMap = tagTester('WeakMap');
var isSet = tagTester('Set');
var isWeakSet = tagTester('WeakSet');

// Define a fallback version of the method in browsers (ahem, IE < 9), where
// there isn't any inspectable "Arguments" type.
(function() {
  if (!isArguments(arguments)) {
    isArguments = function(obj) {
      return _has(obj, 'callee');
    };
  }
}());

// Optimize `isFunction` if appropriate. Work around some typeof bugs in old v8,
// IE 11 (#1621), Safari 8 (#1929), and PhantomJS (#2236).
var nodelist = root.document && root.document.childNodes;
if ( true && typeof Int8Array != 'object' && typeof nodelist != 'function') {
  isFunction = function(obj) {
    return typeof obj == 'function' || false;
  };
}

// Is a given object a finite number?
function isFinite(obj) {
  return !isSymbol(obj) && _isFinite(obj) && !_isNaN(parseFloat(obj));
}

// Is the given value `NaN`?
function isNaN(obj) {
  return isNumber(obj) && _isNaN(obj);
}

// Is a given value a boolean?
function isBoolean(obj) {
  return obj === true || obj === false || toString.call(obj) === '[object Boolean]';
}

// Is a given value equal to null?
function isNull(obj) {
  return obj === null;
}

// Is a given variable undefined?
function isUndefined(obj) {
  return obj === void 0;
}

// Shortcut function for checking if an object has a given property directly
// on itself (in other words, not on a prototype).
function has(obj, path) {
  if (!isArray(path)) {
    return _has(obj, path);
  }
  var length = path.length;
  for (var i = 0; i < length; i++) {
    var key = path[i];
    if (obj == null || !hasOwnProperty.call(obj, key)) {
      return false;
    }
    obj = obj[key];
  }
  return !!length;
}

// Utility Functions
// -----------------

// Keep the identity function around for default iteratees.
function identity(value) {
  return value;
}

// Predicate-generating functions. Often useful outside of Underscore.
function constant(value) {
  return function() {
    return value;
  };
}

function noop(){}

// Creates a function that, when passed an object, will traverse that object’s
// properties down the given `path`, specified as an array of keys or indexes.
function property(path) {
  if (!isArray(path)) {
    return shallowProperty(path);
  }
  return function(obj) {
    return deepGet(obj, path);
  };
}

// Generates a function for a given object that returns a given property.
function propertyOf(obj) {
  if (obj == null) {
    return function(){};
  }
  return function(path) {
    return !isArray(path) ? obj[path] : deepGet(obj, path);
  };
}

// Returns a predicate for checking whether an object has a given set of
// `key:value` pairs.
function matcher(attrs) {
  attrs = extendOwn({}, attrs);
  return function(obj) {
    return isMatch(obj, attrs);
  };
}


// Run a function **n** times.
function times(n, iteratee, context) {
  var accum = Array(Math.max(0, n));
  iteratee = optimizeCb(iteratee, context, 1);
  for (var i = 0; i < n; i++) accum[i] = iteratee(i);
  return accum;
}

// Return a random integer between min and max (inclusive).
function random(min, max) {
  if (max == null) {
    max = min;
    min = 0;
  }
  return min + Math.floor(Math.random() * (max - min + 1));
}

// A (possibly faster) way to get the current timestamp as an integer.
var now = Date.now || function() {
  return new Date().getTime();
};

// List of HTML entities for escaping.
var escapeMap = {
  '&': '&amp;',
  '<': '&lt;',
  '>': '&gt;',
  '"': '&quot;',
  "'": '&#x27;',
  '`': '&#x60;'
};
var unescapeMap = invert(escapeMap);

// Functions for escaping and unescaping strings to/from HTML interpolation.
function createEscaper(map) {
  var escaper = function(match) {
    return map[match];
  };
  // Regexes for identifying a key that needs to be escaped.
  var source = '(?:' + keys(map).join('|') + ')';
  var testRegexp = RegExp(source);
  var replaceRegexp = RegExp(source, 'g');
  return function(string) {
    string = string == null ? '' : '' + string;
    return testRegexp.test(string) ? string.replace(replaceRegexp, escaper) : string;
  };
}
var escape = createEscaper(escapeMap);
var unescape = createEscaper(unescapeMap);

// Traverses the children of `obj` along `path`. If a child is a function, it
// is invoked with its parent as context. Returns the value of the final
// child, or `fallback` if any child is undefined.
function result(obj, path, fallback) {
  if (!isArray(path)) path = [path];
  var length = path.length;
  if (!length) {
    return isFunction(fallback) ? fallback.call(obj) : fallback;
  }
  for (var i = 0; i < length; i++) {
    var prop = obj == null ? void 0 : obj[path[i]];
    if (prop === void 0) {
      prop = fallback;
      i = length; // Ensure we don't continue iterating.
    }
    obj = isFunction(prop) ? prop.call(obj) : prop;
  }
  return obj;
}

// Generate a unique integer id (unique within the entire client session).
// Useful for temporary DOM ids.
var idCounter = 0;
function uniqueId(prefix) {
  var id = ++idCounter + '';
  return prefix ? prefix + id : id;
}

// By default, Underscore uses ERB-style template delimiters, change the
// following template settings to use alternative delimiters.
var templateSettings = _.templateSettings = {
  evaluate: /<%([\s\S]+?)%>/g,
  interpolate: /<%=([\s\S]+?)%>/g,
  escape: /<%-([\s\S]+?)%>/g
};

// When customizing `templateSettings`, if you don't want to define an
// interpolation, evaluation or escaping regex, we need one that is
// guaranteed not to match.
var noMatch = /(.)^/;

// Certain characters need to be escaped so that they can be put into a
// string literal.
var escapes = {
  "'": "'",
  '\\': '\\',
  '\r': 'r',
  '\n': 'n',
  '\u2028': 'u2028',
  '\u2029': 'u2029'
};

var escapeRegExp = /\\|'|\r|\n|\u2028|\u2029/g;

var escapeChar = function(match) {
  return '\\' + escapes[match];
};

// JavaScript micro-templating, similar to John Resig's implementation.
// Underscore templating handles arbitrary delimiters, preserves whitespace,
// and correctly escapes quotes within interpolated code.
// NB: `oldSettings` only exists for backwards compatibility.
function template(text, settings, oldSettings) {
  if (!settings && oldSettings) settings = oldSettings;
  settings = defaults({}, settings, _.templateSettings);

  // Combine delimiters into one regular expression via alternation.
  var matcher = RegExp([
    (settings.escape || noMatch).source,
    (settings.interpolate || noMatch).source,
    (settings.evaluate || noMatch).source
  ].join('|') + '|$', 'g');

  // Compile the template source, escaping string literals appropriately.
  var index = 0;
  var source = "__p+='";
  text.replace(matcher, function(match, escape, interpolate, evaluate, offset) {
    source += text.slice(index, offset).replace(escapeRegExp, escapeChar);
    index = offset + match.length;

    if (escape) {
      source += "'+\n((__t=(" + escape + "))==null?'':_.escape(__t))+\n'";
    } else if (interpolate) {
      source += "'+\n((__t=(" + interpolate + "))==null?'':__t)+\n'";
    } else if (evaluate) {
      source += "';\n" + evaluate + "\n__p+='";
    }

    // Adobe VMs need the match returned to produce the correct offset.
    return match;
  });
  source += "';\n";

  // If a variable is not specified, place data values in local scope.
  if (!settings.variable) source = 'with(obj||{}){\n' + source + '}\n';

  source = "var __t,__p='',__j=Array.prototype.join," +
    "print=function(){__p+=__j.call(arguments,'');};\n" +
    source + 'return __p;\n';

  var render;
  try {
    render = new Function(settings.variable || 'obj', '_', source);
  } catch (e) {
    e.source = source;
    throw e;
  }

  var template = function(data) {
    return render.call(this, data, _);
  };

  // Provide the compiled source as a convenience for precompilation.
  var argument = settings.variable || 'obj';
  template.source = 'function(' + argument + '){\n' + source + '}';

  return template;
}

// Add a "chain" function. Start chaining a wrapped Underscore object.
function chain(obj) {
  var instance = _(obj);
  instance._chain = true;
  return instance;
}

// OOP
// ---------------
// If Underscore is called as a function, it returns a wrapped object that
// can be used OO-style. This wrapper holds altered versions of all the
// underscore functions. Wrapped objects may be chained.

// Helper function to continue chaining intermediate results.
function chainResult(instance, obj) {
  return instance._chain ? _(obj).chain() : obj;
}

// Add your own custom functions to the Underscore object.
function mixin(obj) {
  each(functions(obj), function(name) {
    var func = _[name] = obj[name];
    _.prototype[name] = function() {
      var args = [this._wrapped];
      push.apply(args, arguments);
      return chainResult(this, func.apply(_, args));
    };
  });
  return _;
}

// Add all mutator Array functions to the wrapper.
each(['pop', 'push', 'reverse', 'shift', 'sort', 'splice', 'unshift'], function(name) {
  var method = ArrayProto[name];
  _.prototype[name] = function() {
    var obj = this._wrapped;
    method.apply(obj, arguments);
    if ((name === 'shift' || name === 'splice') && obj.length === 0) delete obj[0];
    return chainResult(this, obj);
  };
});

// Add all accessor Array functions to the wrapper.
each(['concat', 'join', 'slice'], function(name) {
  var method = ArrayProto[name];
  _.prototype[name] = function() {
    return chainResult(this, method.apply(this._wrapped, arguments));
  };
});

// Extracts the result from a wrapped and chained object.
_.prototype.value = function() {
  return this._wrapped;
};

// Provide unwrapping proxy for some methods used in engine operations
// such as arithmetic and JSON stringification.
_.prototype.valueOf = _.prototype.toJSON = _.prototype.value;

_.prototype.toString = function() {
  return String(this._wrapped);
};

/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! ./../../webpack/buildin/global.js */ "./node_modules/webpack/buildin/global.js")))

/***/ }),

/***/ "./node_modules/webpack/buildin/global.js":
/*!***********************************!*\
  !*** (webpack)/buildin/global.js ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

var g;

// This works in non-strict mode
g = (function() {
	return this;
})();

try {
	// This works if eval is allowed (see CSP)
	g = g || new Function("return this")();
} catch (e) {
	// This works if the window reference is available
	if (typeof window === "object") g = window;
}

// g can still be undefined, but nothing to do about it...
// We return undefined, instead of nothing here, so it's
// easier to handle this case. if(!global) { ...}

module.exports = g;


/***/ }),

/***/ "./src/js/actions/changeform_actions.js":
/*!**********************************************!*\
  !*** ./src/js/actions/changeform_actions.js ***!
  \**********************************************/
/*! exports provided: MgChangeFormAction, MgChangeFormActions */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgChangeFormAction", function() { return MgChangeFormAction; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgChangeFormActions", function() { return MgChangeFormActions; });
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../utils */ "./src/js/utils.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _document_form_selection__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../document_form/selection */ "./src/js/document_form/selection.js");
/* harmony import */ var _document_form_clipboard__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../document_form/clipboard */ "./src/js/document_form/clipboard.js");
/* harmony import */ var _node__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../node */ "./src/js/node.js");





/*
  Dropdown menu for document form.
  Menu includes following items:
    * rename - renames the document title
    * page:
        # delete - deletes one or multiple (selected) pages
        # cut - cuts one or multiple selected pages
        # paste - paste pages (which were cut from different document)
*/

class MgChangeFormAction {
  /*
    An abstraction of action item in (actions) dropdown menu from
    changelist and changeform view.
  */
  constructor(config) {
    this._enabled_cond = config['enabled']; // id is a DOM selector (i.e a string)

    this._id = config['id'];
    this._is_enabled = config['initial_state'] || false;
    this._confirm = config['confirm'];
    this._action = config['action'];

    if (this._is_enabled) {
      this.enable();
    }
  }

  get id() {
    return this._id;
  }

  get confirm() {
    return this._confirm;
  }

  get is_enabled() {
    return this._is_enabled;
  }

  enable() {
    this._is_enabled = true;
    jquery__WEBPACK_IMPORTED_MODULE_1___default()(this._id).removeClass("disabled");
  }

  disable() {
    console.log(`${this._id} disabled`);
    this._is_enabled = false;
    jquery__WEBPACK_IMPORTED_MODULE_1___default()(this._id).addClass("disabled");
  }

  toggle(selection, clipboard, current_node, thumbnail_list, page_list) {
    if (this._enabled_cond(selection, clipboard, current_node, thumbnail_list, page_list)) {
      this.enable();
    } else {
      this.disable();
    }
  }

  action(selection, clipboard, current_node, thumbnail_list, page_list) {
    this._action(selection, clipboard, current_node, thumbnail_list, page_list);
  }

}
class MgChangeFormActions {
  /*
    An abstraction of actions dropdown menu in changelist view.
    Actions dropdown menu operates on a selection of one or many
    items (document or folder).
  */
  constructor(thumbnail_list, page_list) {
    let title, id;
    title = jquery__WEBPACK_IMPORTED_MODULE_1___default()("input[name=document_title]").val();
    id = jquery__WEBPACK_IMPORTED_MODULE_1___default()("input[name=document_id]").val();
    this._actions = [];
    this._selection = new _document_form_selection__WEBPACK_IMPORTED_MODULE_2__["MgSelection"](); // user can cut some items in one folder and
    // paste them in another folder. Cut/Pasted items are placed (taken)
    // to/from DgClipboard

    this._clipboard = new _document_form_clipboard__WEBPACK_IMPORTED_MODULE_3__["MgClipboard"]();
    this._current_node = new _node__WEBPACK_IMPORTED_MODULE_4__["DgNode"](id, title);
    this._thumbnail_list = thumbnail_list;
    this._page_list = page_list;
    this.configEvents();
  }

  get selection() {
    return this._selection;
  }

  clear_selection() {
    this.selection.clear();
  }

  add(action) {
    this._attach_events(action);

    this._actions.push(action);
  }

  _attach_events(action) {
    jquery__WEBPACK_IMPORTED_MODULE_1___default()(action.id).click({
      action: action,
      selection: this._selection,
      clipboard: this._clipboard,
      current_node: this._current_node,
      thumbnail_list: this._thumbnail_list,
      page_list: this._page_list
    }, this.on_click);
  }

  on_change_selection(selection) {
    /*
      Invoked every time when selection changes i.e. elemnts are either 
      added or removed from the list.
       Theoretically this._selection and selection should be same.
    */
    for (let action of this._actions) {
      action.toggle(this._selection, this._clipboard, this._current_node, this._thumbnail_list, this._page_list);
    }
  }

  on_change_clipboard(clipboard) {
    console.log(`on_change_clipboard received ${this._selection}`);

    for (let action of this._actions) {
      action.toggle(this._selection, clipboard);
    }
  }

  on_click(event) {
    let action = event.data.action;
    let selection = event.data.selection;
    let clipboard = event.data.clipboard;
    let current_node = event.data.current_node;
    let thumbnail_list = event.data.thumbnail_list;
    let page_list = event.data.page_list;

    if (!action.is_enabled) {
      return;
    }

    action.action(selection, clipboard, current_node, thumbnail_list, page_list);
  }

  configEvents() {
    this._selection.subscribe_event(_document_form_selection__WEBPACK_IMPORTED_MODULE_2__["MgSelection"].CHANGE, this.on_change_selection, this // context
    );

    this._clipboard.subscribe_event(_document_form_clipboard__WEBPACK_IMPORTED_MODULE_3__["MgClipboard"].CHANGE, this.on_change_clipboard, this //context
    );

    for (let action of this._actions) {
      this._attach_events(action);
    }
  }

}

/***/ }),

/***/ "./src/js/app.js":
/*!***********************!*\
  !*** ./src/js/app.js ***!
  \***********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./utils */ "./src/js/utils.js");
/* harmony import */ var _document_form_page_scroll__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./document_form/page_scroll */ "./src/js/document_form/page_scroll.js");
/* harmony import */ var _sort_cookie__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./sort_cookie */ "./src/js/sort_cookie.js");
/* harmony import */ var _views_browse__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./views/browse */ "./src/js/views/browse.js");
/* harmony import */ var _views_breadcrumb__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./views/breadcrumb */ "./src/js/views/breadcrumb.js");
/* harmony import */ var _views_actions__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./views/actions */ "./src/js/views/actions.js");
/* harmony import */ var _views_control_sidebar__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./views/control_sidebar */ "./src/js/views/control_sidebar.js");
/* harmony import */ var _views_document__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./views/document */ "./src/js/views/document.js");
/* harmony import */ var _routers_browse__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./routers/browse */ "./src/js/routers/browse.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var bootstrap_js_dist_util__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! bootstrap/js/dist/util */ "./node_modules/bootstrap/js/dist/util.js");
/* harmony import */ var bootstrap_js_dist_util__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_util__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var bootstrap_js_dist_toast__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! bootstrap/js/dist/toast */ "./node_modules/bootstrap/js/dist/toast.js");
/* harmony import */ var bootstrap_js_dist_toast__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_toast__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var bootstrap_js_dist_tab__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! bootstrap/js/dist/tab */ "./node_modules/bootstrap/js/dist/tab.js");
/* harmony import */ var bootstrap_js_dist_tab__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_tab__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! bootstrap/js/dist/modal */ "./node_modules/bootstrap/js/dist/modal.js");
/* harmony import */ var bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(bootstrap_js_dist_modal__WEBPACK_IMPORTED_MODULE_14__);















let backboneSync = backbone__WEBPACK_IMPORTED_MODULE_9___default.a.sync;

backbone__WEBPACK_IMPORTED_MODULE_9___default.a.sync = function (method, model, options) {
  let csrf_token = jquery__WEBPACK_IMPORTED_MODULE_10___default()("[name=csrfmiddlewaretoken]").val();
  /*
   * The jQuery `ajax` method includes a 'headers' option
   * which lets you set any headers you like
   */

  options.headers = {
    'X-CSRFToken': csrf_token
  };
  /*
   * Call the stored original Backbone.sync method with
   * extra headers argument added
   */

  backboneSync(method, model, options);
};

let App = function () {
  let browse_view, actions_view, breadcrumb_view, document_view, document_actions_view, control_sidebar, browse_router;
  browse_view = new _views_browse__WEBPACK_IMPORTED_MODULE_3__["BrowseView"]();
  actions_view = new _views_actions__WEBPACK_IMPORTED_MODULE_5__["ActionsView"]();
  breadcrumb_view = new _views_breadcrumb__WEBPACK_IMPORTED_MODULE_4__["BreadcrumbView"]();
  control_sidebar = new _views_control_sidebar__WEBPACK_IMPORTED_MODULE_6__["ControlSidebarView"]();

  if (jquery__WEBPACK_IMPORTED_MODULE_10___default()("#document").length == 1) {
    // we in document view. Document view and browser view
    // are exclusive.
    document_view = new _views_document__WEBPACK_IMPORTED_MODULE_7__["DocumentView"]();
    document_actions_view = new _views_document__WEBPACK_IMPORTED_MODULE_7__["DocumentActionsView"]();
  } else {
    browse_router = new _routers_browse__WEBPACK_IMPORTED_MODULE_8__["BrowseRouter"](browse_view, breadcrumb_view, actions_view);
    backbone__WEBPACK_IMPORTED_MODULE_9___default.a.history.start(); // Small notofication popups on top-right corner of the screen.
    // They serve as widgets for django's messages

    jquery__WEBPACK_IMPORTED_MODULE_10___default()('.toast').toast({
      'autohide': false
    });
    jquery__WEBPACK_IMPORTED_MODULE_10___default()('.toast').toast('show');
    Object(_sort_cookie__WEBPACK_IMPORTED_MODULE_2__["sort_cookie"])();
  }
};

Object(_utils__WEBPACK_IMPORTED_MODULE_0__["dglReady"])( // i.e. after all DOM is loaded
function (event) {
  App();
});

/***/ }),

/***/ "./src/js/document_form/clipboard.js":
/*!*******************************************!*\
  !*** ./src/js/document_form/clipboard.js ***!
  \*******************************************/
/*! exports provided: MgClipboard */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgClipboard", function() { return MgClipboard; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../events */ "./src/js/events.js");


class MgClipboard {
  /* 
    List of pages ids to paste into current document.
  */
  constructor(id = "#page_clipboard_form") {
    this._id = id;
    this._list = [];
    this._events = new _events__WEBPACK_IMPORTED_MODULE_1__["DgEvents"]();

    this._get_clipboard_form_server();
  } // event name


  static get CHANGE() {
    return "change";
  }

  subscribe_event(name, handler, context) {
    this._events.subscribe(name, handler, context);
  }

  notify_subscribers(event_name, list) {
    this._events.notify(event_name, list);
  }

  get length() {
    return this._list.length;
  }

  _get_clipboard_form_server() {
    let url = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._id).attr('action');
    let that = this;
    jquery__WEBPACK_IMPORTED_MODULE_0___default.a.get(url, function (data) {
      that._list = data.clipboard;
      that.notify_subscribers(MgClipboard.CHANGE, that._list);
    });
  }

  add(items) {}

  count(cond_fn = x => x) {
    // same as length, but with an optional filter.
    return this._list.filter(cond_fn).length;
  }

}

/***/ }),

/***/ "./src/js/document_form/common.js":
/*!****************************************!*\
  !*** ./src/js/document_form/common.js ***!
  \****************************************/
/*! exports provided: get_win_param, delete_elem_children, is_visible, build_elem, getCookie, csrfSafeMethod */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "get_win_param", function() { return get_win_param; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "delete_elem_children", function() { return delete_elem_children; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "is_visible", function() { return is_visible; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "build_elem", function() { return build_elem; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "getCookie", function() { return getCookie; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "csrfSafeMethod", function() { return csrfSafeMethod; });
function get_win_param(param_name) {
  let searchString = window.location.search.substring(1),
      i,
      val,
      params = searchString.split("&");

  for (i = 0; i < params.length; i++) {
    val = params[i].split("=");

    if (val[0] == param_name) {
      return val[1];
    }
  }

  return null;
}
function delete_elem_children(dom_elem) {
  while (dom_elem.firstChild) {
    dom_elem.removeChild(dom_elem.firstChild);
  }
}
function is_visible(dom_page_item) {
  let rect = dom_page_item.getBoundingClientRect();
  let top_visible = false;
  let bottom_visible = false;
  let top_and_bottom_visible = false;
  let ret;

  if (rect.top >= 0 && rect.top < window.innerHeight) {
    top_visible = true;
  }

  if (rect.bottom >= 0 && rect.bottom <= window.innerHeight) {
    bottom_visible = true;
  }

  if (rect.top <= 0 && rect.bottom >= window.innerHeight) {
    top_and_bottom_visible = true;
  }

  ret = top_visible || bottom_visible || top_and_bottom_visible;
  return top_visible || bottom_visible || top_and_bottom_visible;
}
function build_elem(tag_name, attrs, text = '') {
  let el = document.createElement(tag_name),
      text_content;

  for (let k in attrs) {
    el.setAttribute(k, attrs[k]);
  }

  if (text && text.length > 0) {
    text_content = document.createTextNode(text);
    el.appendChild(text_content);
  }

  return el;
}
function getCookie(name) {
  var cookieValue = null;

  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');

    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim(); // Does this cookie string begin with the name we want?

      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }

  return cookieValue;
}
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return /^(GET|HEAD|OPTIONS|TRACE)$/.test(method);
}

/***/ }),

/***/ "./src/js/document_form/lister.js":
/*!****************************************!*\
  !*** ./src/js/document_form/lister.js ***!
  \****************************************/
/*! exports provided: MgLister */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgLister", function() { return MgLister; });
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../events */ "./src/js/events.js");

class MgLister extends _events__WEBPACK_IMPORTED_MODULE_0__["DgEvents"] {
  /**
      Lister is a common class for MgPageList and MgThumbList.
       Both page lists and thumb lists are updated based on current selection.
      If user triggers delete pages action, boths lists needs to be updated
      accordingly. Same of cut & paste actions.
  */
  constructor() {
    super();
  }

  delete_selected(selection) {
    // selection is instance of 
    // document_form.selection.MgSelection
    let thumbs_to_delete; // extract thumbs using selection object

    thumbs_to_delete = this._list.filter(thumb => selection.contains(thumb)); // remove extracted thumb elements from DOM

    for (let thumb of thumbs_to_delete) {
      $(thumb.dom_ref).remove();
    } // remove elements from list itself


    this.purge_list(selection);
  }

  purge_list(selection) {
    let item, pos;

    for (let sel in selection) {
      pos = this._list.findIndex(x => x.page_id == sel.page_id);

      if (pos >= 0) {
        this._list.splice(pos, 1);
      }
    }
  }

}
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./src/js/document_form/page.js":
/*!**************************************!*\
  !*** ./src/js/document_form/page.js ***!
  \**************************************/
/*! exports provided: MgPage, DgPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgPage", function() { return MgPage; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgPage", function() { return DgPage; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var imagesloaded__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! imagesloaded */ "./node_modules/imagesloaded/imagesloaded.js");
/* harmony import */ var imagesloaded__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(imagesloaded__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./common */ "./src/js/document_form/common.js");
/* harmony import */ var _text_overlay__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../text_overlay */ "./src/js/text_overlay.js");
/* harmony import */ var _rect__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./rect */ "./src/js/document_form/rect.js");
 // imagesloaded will trigger "load" event after img element
// has loaded image. Without this plugin, event WILL NOT
// BE TRIGGERED IF IMG WAS loaded FROM CACHE




 // https://github.com/desandro/imagesloaded#webpack
// make imagesloaded as jquery plugin - this
// enables us to pass dom element reference to imagesloaded function
// (otherwise it accepts only a string query selector)

imagesloaded__WEBPACK_IMPORTED_MODULE_1___default.a.makeJQueryPlugin(jquery__WEBPACK_IMPORTED_MODULE_0___default.a);

function build_text_overlay(dom_page, dom_img, arr_dom_hocr, orig_img_rect, highlight_text_arr) {
  /**
  Creates a semi transparent svg element with text over the image.
  **/
  let overlay;
  overlay = new _text_overlay__WEBPACK_IMPORTED_MODULE_3__["DgTextOverlay"](dom_img, // image over which will build overlay
  dom_page, // dom page item, direct parent of dom_img
  orig_img_rect);
  return overlay.build_for(arr_dom_hocr, highlight_text_arr);
}

class MgPage {
  /**
  Class deals with selection of pages in thumbnail list.
   doc id - server side database id of the associated doc
  page id - server side database id of the page
  page_num - page number when document is displayed in
      the view. It never changes.
  page_order - which is initially = page_num will change
  as user changes the order of the document.
  **/
  constructor(doc_id, page_id, page_num, page_order) {
    this._doc_id = doc_id;
    this._page_id = page_id; // page number is fixed, it does not change.
    // when loading document initially, page_num == page_order
    // if user moves up/down documents => page order changes
    // but page_num no!

    this._page_num = page_num; // page order in the document
    // as opposite to page number (which is fixed),
    // page order changes as user moves page up/down

    this._page_order = page_order;
  }

  get doc_id() {
    return this._doc_id;
  }

  get page_id() {
    return this._page_id;
  }

  get page_order() {
    return this._page_order;
  }

  get page_num() {
    return this._page_num;
  }

  static create_from_dom(dom_elem) {
    let page_order = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".document.page").data("page_order");
    let doc_id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".document.page").data("doc_id");
    let page_id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".document.page").data("page_id");
    let page_num = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".document.page").data("page_num");
    return new MgPage(doc_id, page_id, page_num, page_order);
  }

}
class DgPage {
  /***
      Class deals with OCR layer, scrolling, image loading,
      resizing of the page.
  ***/
  constructor(dom_ref, dom_data_ref, doc_id, page_id, page_num, zoom_val) {
    // .actual_page
    this._dom_ref = dom_ref;
    this._dom_data_ref = dom_data_ref;
    this._dom_img = undefined;
    this._dom_hocr = undefined;
    this._zoom_val = zoom_val;
    this._page_id = page_id;
    this._page_num = page_num;
    this._doc_id = doc_id; // will be known/updated after HOCR for Step(1) is downloaded.

    this._orig_page_size = undefined;
  }

  get dom_ref() {
    return this._dom_ref;
  }

  get page_id() {
    return this._page_id;
  }

  get page_num() {
    return this._page_num;
  }

  replace_with(dom_ref, page_num) {
    this._dom_ref.replaceWith(dom_ref);

    this._dom_ref = dom_ref;
    this._dom_img = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find("img").get(0);
    this._dom_data_ref = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find(".document.page").get(0);
    this._dom_hocr = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find(".page_hocr").get(0);
    this._page_num = page_num;
  }

  highlight_text(text_arr) {
    this._highlight_text_arr = text_arr;
  }

  scroll_to() {
    this._dom_ref.scrollIntoView();
  }

  is_img_loaded() {
    if (this._dom_ref.querySelectorAll('img').length > 0) {
      return true;
    }

    return false;
  }

  is_visible() {
    return Object(_common__WEBPACK_IMPORTED_MODULE_2__["is_visible"])(this._dom_ref);
  }

  set_zoom_val(zoom_val) {
    //console.log(`new zoom val=${zoom_val}`);
    this._zoom_val = zoom_val;
  }

  get_zoom_val() {
    return this._zoom_val;
  }

  load_img(zoom_val) {
    let src,
        dynamic_width,
        arr = [50, 75, 100, 125, 150],
        that = this;
    /*
        Dynamic width is the width of viewer. In will very depending on the
        screen size of user agent.
    */

    dynamic_width = this._dom_ref.getBoundingClientRect().width;
    /*
        value 1 from following url is equivalent of briolette.step.Step(1) on server side.
        Step(1) corresponds to the image of width 1240px.
        By server side convention that is considered 100% width of the image.
        Step(0) will correspond to 125% of Step(1)
        Step(1) ...
        Step(2) will correspond to 75% of Step(1)
        Step(3) will correspond to 50% of Step(1) => image with width=620px.
    */

    src = `/document/${this._doc_id}/preview/1/page/${this._page_num}`;

    if (arr.includes(zoom_val)) {
      dynamic_width = zoom_val / 100 * 1240;
    }

    this._dom_img = Object(_common__WEBPACK_IMPORTED_MODULE_2__["build_elem"])('img', {
      'src': src,
      'width': `${dynamic_width}px`
    });

    this._dom_ref.insertBefore(this._dom_img, this._dom_data_ref // insert before this direct child
    );
    /***
        Tricky one:
        load_hocr(zoom_val) needs to be called, only after
        img element is fully loaded. This is because there is no other
        way in advance to know the height of img element.
        Before img is loaded, img DOM element has height = 0, which
        sets svg proprty to 0 as well.
    ***/


    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_img).imagesLoaded().done(function (instance) {
      that.load_hocr(zoom_val);
    });
  }

  resize_img(zoom_val) {
    let arr = [50, 75, 100, 125, 150],
        new_width;
    console.log(`resize_img zoom_val=${zoom_val}`);

    if (!this._orig_page_size) {
      // image might not yet be loaded, e.g.
      // used opened document and have seen only 
      // first page
      console.log("this.orig_page_size is undefined");
      return;
    }

    if (arr.includes(zoom_val)) {
      new_width = parseInt(zoom_val) / 100 * this._orig_page_size.width;

      this._dom_img.setAttribute('width', `${new_width}px`);

      jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_img).removeAttr('height');
    }

    if (zoom_val == 'width') {
      new_width = this._dom_ref.getBoundingClientRect().width;

      if (this._dom_img) {
        // image might not yet be loaded, e.g.
        // used opened document and have seen only 
        // first page
        this._dom_img.setAttribute('width', `${new_width}px`);
      }

      jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_img).removeAttr('height');
    }
  }

  load_hocr() {
    // load hocr NEEDs to be called only after IMG element
    // was loaded.
    let hocr_url,
        that = this,
        orig_img_width,
        orig_img_height;
    this._dom_hocr = Object(_common__WEBPACK_IMPORTED_MODULE_2__["build_elem"])('div', {
      'class': "page_hocr"
    });
    /**
        value 1 from below url corresponds to briolette.step.Step(1)
    **/

    hocr_url = `/document/${this._doc_id}/hocr/1/page/${this._page_num}`;
    jquery__WEBPACK_IMPORTED_MODULE_0___default.a.ajax({
      url: hocr_url
    }).done(function (data, text_status, jxhr) {
      let dom_span,
          arr_dom_span = [];

      if (jxhr.status != 200) {
        // might return 404 if HOCR data is
        // not ready yet.
        return;
      }

      if (data && data['hocr']) {
        data['hocr'].forEach(function (item, index, arr) {
          dom_span = Object(_common__WEBPACK_IMPORTED_MODULE_2__["build_elem"])('span', {
            'class': item['class'],
            'id': item['id'],
            'title': item['title'],
            'x1': item['x1'],
            'y1': item['y1'],
            'x2': item['x2'],
            'y2': item['y2'],
            'wconf': item['wconf']
          }, item['text']);

          that._dom_hocr.appendChild(dom_span);

          arr_dom_span.push(dom_span);
        });

        that._dom_ref.insertBefore(that._dom_hocr, that._dom_data_ref);

        that._orig_page_size = new _rect__WEBPACK_IMPORTED_MODULE_4__["DgRect"](data['hocr_meta']['width'], data['hocr_meta']['height']);
      }

      that._dom_svg = build_text_overlay(that._dom_ref, that._dom_img, arr_dom_span, that._orig_page_size, that._highlight_text_arr);
    });
  }

  resize_hocr(zoom_val) {
    let hocr_url,
        that = this;

    if (!this._dom_hocr) {
      return;
    } //delete_elem_children(this._dom_hocr);


    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_svg).remove();
    hocr_url = `/document/${this._doc_id}/hocr/1/page/${this._page_num}`;
    jquery__WEBPACK_IMPORTED_MODULE_0___default.a.ajax({
      url: hocr_url
    }).done(function (data) {
      let dom_span,
          arr_dom_span = [],
          highlight_text_arr = [];

      if (data && data['hocr']) {
        data['hocr'].forEach(function (item, index, arr) {
          dom_span = Object(_common__WEBPACK_IMPORTED_MODULE_2__["build_elem"])('span', {
            'class': item['class'],
            'id': item['id'],
            'title': item['title'],
            'x1': item['x1'],
            'y1': item['y1'],
            'x2': item['x2'],
            'y2': item['y2'],
            'wconf': item['wconf']
          }, item['text']);

          that._dom_hocr.appendChild(dom_span);

          arr_dom_span.push(dom_span);
        });
      } // this works, but code logic is brittle.
      // The point is to remap hocr text over image,
      // however, it relies on the fact that image is resized already
      // and when img.getBoundingClientRect() it will take correct target
      // image size.
      // This code wont work is this function is executed BEFORE image is
      // resized.


      that._dom_svg = build_text_overlay(that._dom_ref, that._dom_img, // used to get real image size.
      arr_dom_span, that._orig_page_size, // original image size, as provided by server
      highlight_text_arr);
    });
  }

  on_scroll(zoom_val) {
    if (this.is_visible()) {
      if (!this.is_img_loaded()) {
        this.load_img(zoom_val); // when load_img completes asyncroniously to load
        // image - it triggers load_hocr function.
      } else if (this.zoom_changed(zoom_val)) {
        this.resize_img(zoom_val); // resize happens syncroniously.
        // It means that is ok to call resize_hocr syncr as well.                

        this.resize_hocr(zoom_val);
        this.set_zoom_val(zoom_val);
      }

      this.set_zoom_val(zoom_val);
    }
  }

  viewer_resized() {
    let old_width = this._dom_ref.getBoundingClientRect().width,
        width = this._dom_img.getAttribute('width'),
        ret;

    if (width) {
      width = parseInt(width);
    }

    if (old_width) {
      old_width = parseInt(old_width);
    }

    ret = width != old_width; //console.log(`width=${width} old_width=${old_width} ret=${ret}`);

    return ret;
  }

  zoom_changed(new_zoom_val) {
    let ret;
    ret = new_zoom_val != this.get_zoom_val(); //console.log(`new zoom val = ${new_zoom_val} this.zoom_val = ${this.get_zoom_val()} ret=${ret}`);

    return ret;
  }

  on_zoom(zoom_val) {
    if (this.is_visible()) {
      if (this.zoom_changed(zoom_val) || this.viewer_resized()) {
        this.resize_img(zoom_val);
        this.resize_hocr(zoom_val);
      }
    }

    this.set_zoom_val(zoom_val);
  }

}

/***/ }),

/***/ "./src/js/document_form/page_list.js":
/*!*******************************************!*\
  !*** ./src/js/document_form/page_list.js ***!
  \*******************************************/
/*! exports provided: MgPageList */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgPageList", function() { return MgPageList; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _page__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./page */ "./src/js/document_form/page.js");
/* harmony import */ var _lister__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./lister */ "./src/js/document_form/lister.js");



class MgPageList extends _lister__WEBPACK_IMPORTED_MODULE_2__["MgLister"] {
  constructor(zoom) {
    super();
    this._container_selector = ".actual_pages";
    this._selector = ".actual_pages .actual_page";
    this._list = [];
    this._zoom = zoom;

    this._config_events();
  }

  get zoom() {
    return this._zoom;
  }

  get pages() {
    return this._list;
  }

  get visible_pages() {
    return this._list.filter(page => page.is_visible());
  }

  highlight_text(text_arr) {
    for (let page of this._list) {
      page.highlight_text(text_arr);
    }
  }

  scroll_to(page_num) {
    let arr = [];
    arr = this._list.filter(page => page.page_num == page_num);

    if (arr.length > 0) {
      arr[0].scroll_to();
    }
  }

  load(step) {
    for (let page of this._list) {
      page.on_scroll(step);
    }
  }

  _add_pages() {
    let dom_arr = Array.from(document.querySelectorAll(this._selector));
    let that = this;
    dom_arr.forEach(function (dom_page_item, index, arr) {
      let dom_data = dom_page_item.querySelector('.document.page'),
          doc_id,
          page_num,
          page_id;

      if (!dom_data) {
        console.log("page dom data not found");
        return;
      }

      doc_id = dom_data.getAttribute('data-doc_id');
      page_num = dom_data.getAttribute('data-page_num');
      page_id = dom_data.getAttribute('data-page_id');

      that._list.push(new _page__WEBPACK_IMPORTED_MODULE_1__["DgPage"](dom_page_item, dom_data, doc_id, page_id, page_num));
    });
  }

  on_zoom(new_zoom_val) {
    for (let page of this.pages) {
      // will apply zoom only if page
      // is visible (within view area)
      page.on_zoom(new_zoom_val);
    }
  }

  get_page(page_num) {
    let arr = [];
    arr = this._list.filter(page => page.page_num == page_num);

    if (arr.length > 0) {
      return arr[0];
    }

    return false;
  }

  swap_pages(page_1, page_2) {
    let clone_1, clone_2, dom_data_1, dom_data_2;
    clone_1 = jquery__WEBPACK_IMPORTED_MODULE_0___default()(page_1.dom_ref).clone();
    clone_2 = jquery__WEBPACK_IMPORTED_MODULE_0___default()(page_2.dom_ref).clone();
    page_1.replace_with(clone_2[0], page_2.page_num);
    page_2.replace_with(clone_1[0], page_1.page_num);
  }

  on_page_move_down(page_num, doc_id, page_id) {
    let page_1, page_2;
    page_1 = this.get_page(page_num);
    page_2 = this.get_page(page_num + 1);
    this.swap_pages(page_1, page_2);
  }

  on_page_move_up(page_num, doc_id, page_id) {
    let page_1, page_2;
    page_1 = this.get_page(page_num);
    page_2 = this.get_page(page_num - 1);
    this.swap_pages(page_1, page_2);
  }

  _config_events() {
    let that = this;

    this._add_pages();

    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._container_selector).scroll(function () {
      for (let page of that._list) {
        page.on_scroll(that.zoom.get_value());
      }
    });
  }

}

/***/ }),

/***/ "./src/js/document_form/page_scroll.js":
/*!*********************************************!*\
  !*** ./src/js/document_form/page_scroll.js ***!
  \*********************************************/
/*! exports provided: DgPageScroll */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgPageScroll", function() { return DgPageScroll; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);

class DgPageScroll {
  constructor(dom_ref, speed = 0.25) {
    this._dom_ref = dom_ref;
    this._is_active = false;
    this._startX = 0;
    this._startY = 0;
    this._scrollLeft = this._dom_ref.scrollLeft;
    this._scrollTop = this._dom_ref.scrollTop;
    this._speed = speed;

    this._config_events();
  }

  _config_events() {
    let that = this;

    this._dom_ref.addEventListener('mousedown', e => {
      // dont scroll when user wants to select text
      // i.e. hovers mouse over <text> element.
      if (e.srcElement.tagName == 'text') {
        that._is_active = false;
        return;
      }

      that._is_active = true;
      that._startX = e.pageX - that._dom_ref.offsetLeft;
      that._startY = e.pageY - that._dom_ref.offsetTop;
    });

    this._dom_ref.addEventListener('mouseleave', () => {
      that._is_active = false;
    });

    this._dom_ref.addEventListener('mouseup', () => {
      that._is_active = false;
    });

    this._dom_ref.addEventListener('mousemove', e => {
      if (!that._is_active) {
        return;
      }

      e.preventDefault();
      const x = e.pageX - that._dom_ref.offsetLeft;
      const y = e.pageY - that._dom_ref.offsetTop;
      const walk_x = x - that._startX;
      const walk_y = y - that._startY;
      that._dom_ref.scrollLeft = that._dom_ref.scrollLeft - walk_x * that._speed;
      that._dom_ref.scrollTop = that._dom_ref.scrollTop - walk_y * that._speed;
    });
  }

}

/***/ }),

/***/ "./src/js/document_form/rect.js":
/*!**************************************!*\
  !*** ./src/js/document_form/rect.js ***!
  \**************************************/
/*! exports provided: DgRect */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgRect", function() { return DgRect; });
class DgRect {
  /**
      A rectangle has a width and a height
      measured in pixels.
      It is more practical to pass
      one single instance of rect instead
      of having width and height separate.
  **/
  constructor(width, height) {
    this._width = parseInt(width);
    this._height = parseInt(height);
  }

  get width() {
    return this._width;
  }

  get height() {
    return this._height;
  }

}

/***/ }),

/***/ "./src/js/document_form/selection.js":
/*!*******************************************!*\
  !*** ./src/js/document_form/selection.js ***!
  \*******************************************/
/*! exports provided: MgSelection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgSelection", function() { return MgSelection; });
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../events */ "./src/js/events.js");
/* harmony import */ var _page__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./page */ "./src/js/document_form/page.js");


class MgSelection {
  // digilette (dg) was renamed to papermerge (mg)

  /**
  A list of selected pages from current document
  **/
  static get DELETE() {
    return "mg_delete_selected_page";
  } // event name


  static get CHANGE() {
    return "mg_selection_changed";
  }

  constructor() {
    this._list = [];
    this._events = new _events__WEBPACK_IMPORTED_MODULE_0__["DgEvents"]();

    this._configEvents();
  }

  subscribe_event(name, handler, context) {
    this._events.subscribe(name, handler, context);
  }

  notify_subscribers(event_name) {
    this._events.notify(event_name);
  }

  clear() {
    this._list = [];

    this._configEvents();

    this.notify_subscribers(MgSelection.CHANGE, this._list);
  }

  contains(item) {
    let pos;
    pos = this._list.findIndex(x => x.page_id == item.page_id);
    return pos >= 0;
  }

  add(mg_page) {
    let pos;
    pos = this._list.findIndex(item => item.page_id == mg_page.page_id); // add mg_page only if it is not already in the list.

    if (pos < 0) {
      this._list.push(mg_page);
    }
  }

  all() {
    return this._list;
  }

  first() {
    return this._list[0];
  }

  remove(mg_page) {
    let pos;
    pos = this._list.findIndex(item => item.page_num == mg_page.page_num);

    if (pos >= 0) {
      this._list.splice(pos, 1);
    }
  }

  get length() {
    return this._list.length;
  }

  _on_page_click(event) {
    let $this = $(this);
    let mg_page;
    let checkbox = $this.find("[type=checkbox]").first();
    let checked, new_state;
    checked = checkbox.prop("checked");
    new_state = !checked;
    checkbox.prop("checked", new_state);

    if (new_state) {
      $this.addClass("checked");
    } else {
      $this.removeClass("checked");
    }

    mg_page = _page__WEBPACK_IMPORTED_MODULE_1__["MgPage"].create_from_dom($this);

    if (new_state) {
      // is checked
      event.data.selection.add(mg_page);
    } else {
      event.data.selection.remove(mg_page);
    }

    event.data.selection.notify_subscribers(MgSelection.CHANGE, this._list);
  }

  _configEvents() {
    // listens on clicks on file and folders
    // and adds/removes them from list
    // when selection count changed - sends an event
    $(".page_thumbnail").unbind('click');
    $(".page_thumbnail").click({
      selection: this
    }, this._on_page_click);
  }

}
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./src/js/document_form/thumbnail.js":
/*!*******************************************!*\
  !*** ./src/js/document_form/thumbnail.js ***!
  \*******************************************/
/*! exports provided: MgThumbnail */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgThumbnail", function() { return MgThumbnail; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../events */ "./src/js/events.js");
/* harmony import */ var _common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./common */ "./src/js/document_form/common.js");



class MgThumbnail extends _events__WEBPACK_IMPORTED_MODULE_1__["DgEvents"] {
  /**
  On single clicks - thumbnails are included/removed to selection.
  On double clicks - view will scroll to tumbnail's page.
   Thus, single clicks are about managing selection of thumbnails/pages, while
  double clicks are about scrolling pages.
  **/
  // event name
  static get CLICK() {
    return "click";
  } // event name


  static get DBLCLICK() {
    return "dblclick";
  }

  static get MOVE_UP() {
    return "move_up";
  }

  static get MOVE_DOWN() {
    return "move_down";
  } // if two consecutive clicks occur in less than CLICK_TIMEOUT miliseconds
  // they will be classified as "double click".


  static get CLICK_TIMEOUT() {
    return 250; // miliseconds
  }

  static get_data_ref_from_dom(dom_ref) {
    let dom_data_ref = dom_ref.querySelector('.document.page');

    if (!dom_data_ref) {
      console.log("thumb dom data not found");
      return;
    }

    return dom_data_ref;
  }

  static get_data_from_dom(dom_ref) {
    let dom_data = dom_ref.querySelector('.document.page'),
        data = {};

    if (!dom_data) {
      console.log("thumb dom data not found");
      return;
    }

    data['doc_id'] = dom_data.getAttribute('data-doc_id');
    data['page_num'] = dom_data.getAttribute('data-page_num');
    data['page_id'] = dom_data.getAttribute('data-page_id');
    data['page_order'] = dom_data.getAttribute('data-page_order');
    return data;
  }

  constructor(dom_ref, dom_data_ref, doc_id, page_id, page_num) {
    super();
    this._dom_ref = dom_ref;
    this._dom_data_ref = dom_data_ref;
    this._step = 4;
    this._page_num = page_num;
    this._page_id = page_id;
    this._doc_id = doc_id;

    this._config_events();
  }

  replace_with(dom_ref) {
    let dom_data = MgThumbnail.get_data_from_dom(dom_ref),
        dom_data_ref = MgThumbnail.get_data_ref_from_dom(dom_ref);

    this._dom_ref.replaceWith(dom_ref);

    this._dom_ref = dom_ref;

    if (!dom_data) {
      console.log("dom_data empty");
      return;
    } // Do not carry on page_num attribute
    // it is a bug to do so.
    // When page order changes - page number attributes
    // changes as well.
    //this._page_num = dom_data['page_num'];


    this._page_id = dom_data['page_id'];
    this._dom_data_ref = dom_data_ref; // reconfigure events for this thumbnail

    dom_data_ref.setAttribute('data-page_order', this._page_num);

    this._config_events();
  }

  get dom_ref() {
    return this._dom_ref;
  }

  get doc_id() {
    return this._doc_id;
  }

  get page_id() {
    return this._page_id;
  }

  get page_num() {
    return this._page_num;
  }

  add_class(css_class) {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this.dom_ref).addClass(css_class);
  }

  remove_class(css_class) {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this.dom_ref).removeClass(css_class);
  }

  mark_highlight() {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).addClass('current');
  }

  remove_highlight() {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).removeClass('current');
  }

  clear_selection() {
    let checkbox;
    checkbox = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find("[type=checkbox]").first();
    checkbox.prop("checked", false);
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).removeClass('checked');
  }

  _config_events() {
    let that = this;
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find(".arrow-up-control").click(function (e) {
      e.preventDefault();
      that.notify(MgThumbnail.MOVE_UP, that._page_num, that.doc_id, that.page_id);
    });
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_ref).find(".arrow-down-control").click(function (e) {
      e.preventDefault();
      that.notify(MgThumbnail.MOVE_DOWN, that._page_num, that.doc_id, that.page_id);
    });

    this._dom_ref.onclick = function () {
      // single click or dblclick?
      if (that.timer) {
        // This way, if click is already set to fire,
        // it will clear itself to avoid duplicate 'Single' alerts.
        clearTimeout(that.timer);
      }

      that.timer = setTimeout(function () {
        that.notify(MgThumbnail.CLICK, that._page_num, that.doc_id, that.page_id);
      }, MgThumbnail.CLICK_TIMEOUT);
    };

    this._dom_ref.ondblclick = function () {
      if (that.timer) {
        clearTimeout(that.timer);
      }

      that.notify(MgThumbnail.DBLCLICK, that._page_num);
    };
  }

  onclick(handler, context) {
    this.subscribe(MgThumbnail.CLICK, handler, context);
  }

  ondblclick(handler, context) {
    this.subscribe(MgThumbnail.DBLCLICK, handler, context);
  }

  is_img_loaded() {
    if (this._dom_ref.querySelectorAll('img').length > 0) {
      return true;
    }

    return false;
  }

  is_visible() {
    return Object(_common__WEBPACK_IMPORTED_MODULE_2__["is_visible"])(this._dom_ref);
  }

  load() {
    if (this.is_img_loaded()) {
      return;
    }

    this.load_img();
  }

  load_img() {
    let dom_img, src;
    src = `/document/${this._doc_id}/preview/${this._step}/page/${this._page_num}`;
    dom_img = Object(_common__WEBPACK_IMPORTED_MODULE_2__["build_elem"])('img', {
      'src': src
    });

    this._dom_ref.insertBefore(dom_img, this._dom_data_ref // insert before this direct child
    );
  }

  on_scroll() {
    if (this.is_visible()) {
      this.load();
    }
  }

}

/***/ }),

/***/ "./src/js/document_form/thumbnail_list.js":
/*!************************************************!*\
  !*** ./src/js/document_form/thumbnail_list.js ***!
  \************************************************/
/*! exports provided: MgThumbnailList */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MgThumbnailList", function() { return MgThumbnailList; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _thumbnail__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./thumbnail */ "./src/js/document_form/thumbnail.js");
/* harmony import */ var _lister__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./lister */ "./src/js/document_form/lister.js");
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");




class MgThumbnailList extends _lister__WEBPACK_IMPORTED_MODULE_2__["MgLister"] {
  constructor() {
    super();
    this._container_selector = ".page_thumbnails";
    this._selector = ".page_thumbnails .page_thumbnail";
    this._list = [];

    this._config_events();
  }

  load() {
    for (let thumb of this._list) {
      thumb.on_scroll();
    }
  }

  all() {
    return this._list;
  }

  ondblclick(handler, context) {
    for (let thumb of this._list) {
      thumb.ondblclick(handler, context);
    }
  }

  onclick(handler, context) {
    for (let thumb of this._list) {
      thumb.onclick(handler, context);
    }
  }

  remove_highlights() {
    for (let thumb of this._list) {
      thumb.remove_highlight();
    }
  }

  clear_selections() {
    for (let thumb of this._list) {
      thumb.clear_selection();
    }
  }

  get_thumb(page_num) {
    let arr = [];
    arr = this._list.filter(thumb => thumb.page_num == page_num);

    if (arr.length > 0) {
      return arr[0];
    }

    return false;
  }

  swap_thumbs(thumb_1, thumb_2) {
    let clone_1, clone_2, dom_data_1, dom_data_2;
    clone_1 = jquery__WEBPACK_IMPORTED_MODULE_0___default()(thumb_1.dom_ref).clone();
    clone_2 = jquery__WEBPACK_IMPORTED_MODULE_0___default()(thumb_2.dom_ref).clone();
    thumb_1.replace_with(clone_2[0]);
    thumb_2.replace_with(clone_1[0]);
    this.update_css_class(thumb_1);
    this.update_css_class(thumb_2);
  }

  update_css_class(thumb) {
    if (this.is_first(thumb)) {
      thumb.add_class('first');
    } else {
      thumb.remove_class('first');
    }

    if (this.is_last(thumb)) {
      thumb.add_class('last');
    } else {
      thumb.remove_class('last');
    }
  }

  is_first(thumb) {
    return thumb.page_num == 1;
  }

  is_last(thumb) {
    return thumb.page_num == this._list.length;
  }

  mark_highlight(page_num) {
    /**
        Mark thumbnail as current page in the view.
    **/
    let thumb;
    thumb = this.get_thumb(page_num);

    if (thumb) {
      thumb.mark_highlight();
    }
  }

  on_thumb_move_up(page_num, doc_id, page_id) {
    let thumb_1, thumb_2;

    if (page_num) {
      page_num = parseInt(page_num, 10);
    }

    if (!page_num) {
      console.warning("page_num not a number");
      return;
    }

    if (page_num < 2) {
      // one page document, discard, do nothing.
      // or maybe first page
      return false;
    }

    thumb_1 = this.get_thumb(page_num);
    thumb_2 = this.get_thumb(page_num - 1); // because page_num >=2

    this.swap_thumbs(thumb_1, thumb_2);
    this.notify(_thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].MOVE_UP, page_num, doc_id, page_id);
  }

  on_thumb_move_down(page_num, doc_id, page_id) {
    let thumb_1, thumb_2;

    if (page_num) {
      page_num = parseInt(page_num, 10);
    }

    if (!page_num) {
      console.warning("page_num not a number");
      return;
    }

    if (page_num > this._list.length - 1) {
      return false;
    }

    thumb_1 = this.get_thumb(page_num);
    thumb_2 = this.get_thumb(page_num + 1); // because page_num >=2

    this.swap_thumbs(thumb_1, thumb_2);
    this.notify(_thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].MOVE_DOWN, page_num, doc_id, page_id);
  }

  _add_thumbnails() {
    let dom_arr = Array.from(document.querySelectorAll(this._selector));
    let that = this,
        thumb;
    dom_arr.forEach(function (dom_page_item, index, arr) {
      let dom_data, dom_data_ref;
      dom_data = _thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].get_data_from_dom(dom_page_item);
      dom_data_ref = _thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].get_data_ref_from_dom(dom_page_item);

      if (!dom_data) {
        console.log("thumb dom data not found");
        return;
      }

      thumb = new _thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"](dom_page_item, dom_data_ref, dom_data['doc_id'], dom_data['page_id'], dom_data['page_num']);
      thumb.subscribe(_thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].MOVE_UP, that.on_thumb_move_up, that);
      thumb.subscribe(_thumbnail__WEBPACK_IMPORTED_MODULE_1__["MgThumbnail"].MOVE_DOWN, that.on_thumb_move_down, that);

      that._list.push(thumb);
    });
  }

  _config_events() {
    let that = this,
        first_thumb;

    this._add_thumbnails();

    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._container_selector).scroll(function () {
      for (let thumb of that._list) {
        thumb.on_scroll();
      }
    }); // after document load, user did not select
    // any page yet. In this case, metadata view will
    // display first page' metadata.

    if (this._list.length > 0) {
      // if there is at least one thumbnail
      first_thumb = this._list[0];
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["PAGE_SELECTION_CHANGED"], first_thumb.page_id);
    }
  }

}

/***/ }),

/***/ "./src/js/document_form/zoom.js":
/*!**************************************!*\
  !*** ./src/js/document_form/zoom.js ***!
  \**************************************/
/*! exports provided: DgZoom */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgZoom", function() { return DgZoom; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _events__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../events */ "./src/js/events.js");


let WIDTH = "width";
class DgZoom extends _events__WEBPACK_IMPORTED_MODULE_1__["DgEvents"] {
  constructor(dom_class = ".zoom") {
    // there might be two ".zoom" elements
    // one displayed for mobile view, another one
    // for desktop view.
    super();
    this._dom_ref = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_class);
    this._value = WIDTH; //default value

    this._configEvents();
  }

  set_value(zoom_val) {
    if (zoom_val == WIDTH) {
      this._value = WIDTH;
    } else {
      this._value = parseInt(zoom_val);
    }
  }

  get_value() {
    return this._value;
  }

  _configEvents() {
    let that = this;

    this._dom_ref.change(function () {
      let zoom_val = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).val();
      that.set_value(zoom_val);
      that.notify("zoom", that.get_value());
    });
  }

}

/***/ }),

/***/ "./src/js/events.js":
/*!**************************!*\
  !*** ./src/js/events.js ***!
  \**************************/
/*! exports provided: DgEvents */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgEvents", function() { return DgEvents; });
class DgEvents {
  constructor() {
    this._events = {};
  }

  subscribe(name, handler, context) {
    let event = {
      handler,
      context
    };

    if (this._events[name]) {
      this._events[name].push(event);
    } else {
      this._events[name] = [event];
    }
  } // ...args = Rest parameters syntax
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Functions/rest_parameters


  notify(event_name, ...args) {
    let events = this._events[event_name];

    if (events) {
      for (let event of events) {
        event.handler.apply(event.context, args);
      }
    }
  }

}

/***/ }),

/***/ "./src/js/models/access.js":
/*!*********************************!*\
  !*** ./src/js/models/access.js ***!
  \*********************************/
/*! exports provided: AccessCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AccessCollection", function() { return AccessCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _models_permission__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/permission */ "./src/js/models/permission.js");




class AccessCollection extends backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"] {
  /****
      All access for specific node
  ****/
  get model() {
    return _models_permission__WEBPACK_IMPORTED_MODULE_3__["Permission"];
  }

  initialize(model, options) {
    if (options) {
      this.node = options.node;
    }
  }

  url() {
    if (this.node) {
      return `/node/${this.node.id}/access`;
    }
  }

  parse(response, options) {
    let access = response.access,
        that = this; // do not trigger reset event

    that.reset([], {
      'silent': true
    });

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(access, function (item) {
      that.add(new _models_permission__WEBPACK_IMPORTED_MODULE_3__["Permission"](item));
    });

    this.trigger('change');
    return access;
  }

  save_access(deleted_collection) {
    let token, post_data, request;
    token = jquery__WEBPACK_IMPORTED_MODULE_1___default()("[name=csrfmiddlewaretoken]").val();
    post_data = {
      'add': [],
      'delete': []
    };
    post_data['add'] = this.models.map(function (models) {
      return models.attributes;
    });
    post_data['delete'] = deleted_collection.models.map(function (models) {
      return models.attributes;
    });
    jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajaxSetup({
      headers: {
        'X-CSRFToken': token
      }
    });
    request = jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajax({
      method: "POST",
      url: this.url(),
      data: JSON.stringify(post_data),
      contentType: "application/json",
      dataType: 'json'
    });
  }

}

/***/ }),

/***/ "./src/js/models/breadcrumb.js":
/*!*************************************!*\
  !*** ./src/js/models/breadcrumb.js ***!
  \*************************************/
/*! exports provided: Breadcrumb */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Breadcrumb", function() { return Breadcrumb; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./node */ "./src/js/models/node.js");
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");




class Breadcrumb extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      nodes: [],
      parent_id: ''
    };
  }

  initialize(parent_id) {
    this.set({
      'parent_id': parent_id
    });
    this.nodes = new _node__WEBPACK_IMPORTED_MODULE_2__["NodeCollection"]();
  }

  urlRoot() {
    let parent_id = this.get('parent_id');

    if (parent_id) {
      return `/breadcrumb/${parent_id}/`;
    }

    return '/breadcrumb/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      parent_id: this.get('parent_id'),
      nodes: this.get('nodes')
    };
    return dict;
  }

  open(parent_node, notify_all) {
    let parent_id;

    if (parent_node) {
      parent_id = parent_node.id;
    } else {
      parent_id = undefined;
    }

    this.set({
      'parent_id': parent_id
    });

    if (notify_all) {
      // inform everybody about new parent
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["PARENT_CHANGED"], parent_id);
    }
  }

  parse(response, options) {
    let nodes = response.nodes,
        that = this;
    that.nodes.reset();

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(nodes, function (item) {
      that.nodes.add(new _node__WEBPACK_IMPORTED_MODULE_2__["Node"](item));
    });

    this.trigger('change');
  }

}

/***/ }),

/***/ "./src/js/models/browse.js":
/*!*********************************!*\
  !*** ./src/js/models/browse.js ***!
  \*********************************/
/*! exports provided: Browse */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Browse", function() { return Browse; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./node */ "./src/js/models/node.js");
/* harmony import */ var _kvstore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./kvstore */ "./src/js/models/kvstore.js");
/* harmony import */ var _dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dispatcher */ "./src/js/models/dispatcher.js");





class Browse extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      nodes: [],
      parent_id: '',
      parent_kv: [] // used in list display mode

    };
  }

  initialize(parent_id) {
    this.parent_id = parent_id;
    this.nodes = new _node__WEBPACK_IMPORTED_MODULE_2__["NodeCollection"]();
    this.parent_kv = new _kvstore__WEBPACK_IMPORTED_MODULE_3__["KVStoreCollection"]();
  }

  urlRoot() {
    let parent_id = this.get('parent_id');

    if (parent_id) {
      return `/browse/${parent_id}/`;
    }

    return '/browse/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      parent_id: this.get('parent_id'),
      nodes: this.get('nodes')
    };
    return dict;
  }

  open(parent_node, notify_all) {
    let parent_id;

    if (parent_node) {
      parent_id = parent_node.id;
    } else {
      parent_id = undefined;
    }

    this.set({
      'parent_id': parent_id
    });

    if (notify_all) {
      // inform everybody about new parent
      _dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_dispatcher__WEBPACK_IMPORTED_MODULE_4__["PARENT_CHANGED"], parent_id);
    }
  }

  parse(response, options) {
    let nodes = response.nodes,
        that = this,
        parent_kv = response.parent_kv,
        parent_id = response.parent_id;
    that.nodes.reset();

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(nodes, function (item) {
      that.nodes.add(new _node__WEBPACK_IMPORTED_MODULE_2__["Node"](item));
    });

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(parent_kv, function (item) {
      that.parent_kv.add(new _kvstore__WEBPACK_IMPORTED_MODULE_3__["KVStore"](item));
    });

    this.set({
      'parent_id': parent_id
    });
    this.trigger('change');
  }

}

/***/ }),

/***/ "./src/js/models/dispatcher.js":
/*!*************************************!*\
  !*** ./src/js/models/dispatcher.js ***!
  \*************************************/
/*! exports provided: mg_dispatcher, PARENT_CHANGED, SELECTION_CHANGED, PAGE_SELECTION_CHANGED, BROWSER_REFRESH, PERMISSION_CHANGED */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "mg_dispatcher", function() { return mg_dispatcher; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PARENT_CHANGED", function() { return PARENT_CHANGED; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SELECTION_CHANGED", function() { return SELECTION_CHANGED; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PAGE_SELECTION_CHANGED", function() { return PAGE_SELECTION_CHANGED; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BROWSER_REFRESH", function() { return BROWSER_REFRESH; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PERMISSION_CHANGED", function() { return PERMISSION_CHANGED; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);


let mg_dispatcher = underscore__WEBPACK_IMPORTED_MODULE_0__["default"].clone(backbone__WEBPACK_IMPORTED_MODULE_1__["Events"]);
let PARENT_CHANGED = "parent_changed"; // selection changed event is used to refresh metadata view
// for nodes i.e. while user is browsing documents and folders.

let SELECTION_CHANGED = "selection_changed"; // page_selection_changed event is used to refresh metadata view
// in DOCUMENT VIEWER. In Document viewer, it is displayed is per Page
// If nothing is selected - metadata for first page is displayed.

let PAGE_SELECTION_CHANGED = "page_selection_changed";
let BROWSER_REFRESH = "browser_refresh";
let PERMISSION_CHANGED = "permission_changed";

/***/ }),

/***/ "./src/js/models/document.js":
/*!***********************************!*\
  !*** ./src/js/models/document.js ***!
  \***********************************/
/*! exports provided: Document */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Document", function() { return Document; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _page__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./page */ "./src/js/models/page.js");
/* harmony import */ var _thumbnail__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./thumbnail */ "./src/js/models/thumbnail.js");
/* harmony import */ var _dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./dispatcher */ "./src/js/models/dispatcher.js");





class Document extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      pages: [],
      doc_id: ''
    };
  }

  initialize(id) {
    this.set({
      'id': id
    });
    this.pages = new _page__WEBPACK_IMPORTED_MODULE_2__["PageCollection"]();
    this.thumbnails = new _thumbnail__WEBPACK_IMPORTED_MODULE_3__["ThumbnailCollection"]();
  }

  urlRoot() {
    return `/document/`;
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      nodes: this.get('pages')
    };
    return dict;
  }

  parse(response, options) {
    let pages = response.document.pages,
        that = this;
    that.pages.reset();

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(pages, function (item) {
      that.pages.add(new _page__WEBPACK_IMPORTED_MODULE_2__["Page"](item));
    });

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(pages, function (item) {
      that.thumbnails.add(new _thumbnail__WEBPACK_IMPORTED_MODULE_3__["Thumbnail"](item));
    });

    this.set({
      'title': response.document.title
    });
    this.set({
      'notes': response.document.notes
    });
    this.trigger('change');
  }

}

/***/ }),

/***/ "./src/js/models/kvstore.js":
/*!**********************************!*\
  !*** ./src/js/models/kvstore.js ***!
  \**********************************/
/*! exports provided: KVStore, KVStoreCollection, KVStoreComp, KVStoreCompCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "KVStore", function() { return KVStore; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "KVStoreCollection", function() { return KVStoreCollection; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "KVStoreComp", function() { return KVStoreComp; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "KVStoreCompCollection", function() { return KVStoreCompCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);


class KVStore extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      key: '',
      value: '',
      virtual_value: '',
      kv_inherited: false,
      kv_type: 'text',
      kv_format: undefined
    };
  }

  initialize(doc_id) {
    this.on('change:kv_type', this.update_current_formats);
    this.trigger('change:kv_type');
  }

  update_current_formats() {
    if (this.get('kv_type') == 'date') {
      this.set('current_formats', this.get('date_formats'));
    } else if (this.get('kv_type') == 'money') {
      this.set('current_formats', this.get('currency_formats'));
    } else if (this.get('kv_type') == 'numeric') {
      this.set('current_formats', this.get('numeric_formats'));
    } else {
      this.set('current_formats', []);
    }
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      key: this.get('key'),
      value: this.get('value'),
      virtual_value: this.get('virtual_value'),
      kv_inherited: this.get('kv_inherited'),
      kv_type: this.get('kv_type'),
      kv_format: this.get('kv_format')
    };
    return dict;
  }

  get disabled() {
    // used to disable input form for inherited
    // kv items
    if (this.get('kv_inherited')) {
      return 'disabled';
    }

    return '';
  }

}
class KVStoreCollection extends backbone__WEBPACK_IMPORTED_MODULE_1__["Collection"] {
  get model() {
    return KVStore;
  }

}
class KVStoreComp extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      id: '',
      key: '',
      kv_inherited: false,
      kv_type: 'text',
      kv_format: undefined,
      // only used on local, not passed to the server
      current_formats: []
    };
  }

  toJSON() {
    let dict = {
      key: this.get('key'),
      kv_inherited: this.get('kv_inherited'),
      kv_type: this.get('kv_type'),
      kv_format: this.get('kv_format')
    };
    return dict;
  }

}
class KVStoreCompCollection extends backbone__WEBPACK_IMPORTED_MODULE_1__["Collection"] {
  get model() {
    return KVStoreComp;
  }

}

/***/ }),

/***/ "./src/js/models/metadata.js":
/*!***********************************!*\
  !*** ./src/js/models/metadata.js ***!
  \***********************************/
/*! exports provided: Metadata */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Metadata", function() { return Metadata; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _kvstore__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./kvstore */ "./src/js/models/kvstore.js");




let CSRF_TOKEN = $("[name=csrfmiddlewaretoken]").val();
Backbone.$.ajaxSetup({
  headers: {
    'X-CSRFToken': CSRF_TOKEN
  }
});
class Metadata extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      kvstore: new _kvstore__WEBPACK_IMPORTED_MODULE_2__["KVStoreCollection"](),
      kv_types: [],
      date_formats: [],
      currency_formats: [],
      numeric_formats: []
    };
  }

  initialize(doc_id) {
    this.doc_id = doc_id; // fetch data from server side

    this.fetch();
  }

  get kvstore() {
    return this.get('kvstore');
  }

  get all_disabled() {
    let kvstore = this.get('kvstore'),
        inherited_items = [];
    inherited_items = underscore__WEBPACK_IMPORTED_MODULE_0__["default"].filter(kvstore.models, function (model) {
      return model.get('kv_inherited') == true;
    }); // if all items in kvstore are disabled

    if (inherited_items.length == kvstore.length) {
      return true;
    }

    return false;
  }

  urlRoot() {
    return `/metadata/node/${this.doc_id}`;
  }

  toJSON() {
    let dict = {};
    dict['kvstore'] = this.kvstore.toJSON();
    return dict;
  }

  parse(response, options) {
    let kvstore = response.kvstore,
        kv_types = response.kv_types,
        date_formats = response.date_formats,
        numeric_formats = response.numeric_formats,
        currency_formats = response.currency_formats,
        that = this;

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(kvstore, function (item) {
      that.kvstore.add(new _kvstore__WEBPACK_IMPORTED_MODULE_2__["KVStore"](item));
    });

    this.set({
      'kv_types': kv_types
    });
    this.set({
      'numeric_formats': numeric_formats
    });
    this.set({
      'date_formats': date_formats
    });
    this.set({
      'currency_formats': currency_formats
    });
    this.trigger('change');
  }

  update_simple(cid, attr, value) {
    let model = this.kvstore.get(cid),
        dict = {};

    if (model && attr) {
      dict[attr] = value;
      model.set(dict);
    }
  }

  add_simple() {
    this.kvstore.add(new _kvstore__WEBPACK_IMPORTED_MODULE_2__["KVStore"]({
      'kv_current_formats': this.kv_current_formats,
      'kv_types': this.kv_types
    }));
  }

  remove_simple(cid) {
    this.kvstore.remove({
      'cid': cid
    });
  }

  remove_comp(cid) {
    this.kvstore_comp.remove({
      'cid': cid
    });
  }

}
;
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./src/js/models/metadata_page.js":
/*!****************************************!*\
  !*** ./src/js/models/metadata_page.js ***!
  \****************************************/
/*! exports provided: MetadataPage */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MetadataPage", function() { return MetadataPage; });
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./metadata */ "./src/js/models/metadata.js");

class MetadataPage extends _metadata__WEBPACK_IMPORTED_MODULE_0__["Metadata"] {
  initialize(page_id) {
    this.page_id = page_id; // fetch data from server side

    this.fetch();
  }

  urlRoot() {
    return `/metadata/page/${this.page_id}`;
  }

}
;

/***/ }),

/***/ "./src/js/models/new_folder.js":
/*!*************************************!*\
  !*** ./src/js/models/new_folder.js ***!
  \*************************************/
/*! exports provided: NewFolder */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NewFolder", function() { return NewFolder; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);


class NewFolder extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  /**
      Used for new folder/rename node operations.
  */
  defaults() {
    return {
      title: '',
      parent_id: ''
    };
  }

  initialize(parent_id) {
    this.set({
      'parent_id': parent_id
    });
  }

  urlRoot() {
    return '/create-folder/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      parent_id: this.get('parent_id'),
      title: this.get('title')
    };
    return dict;
  }

}

/***/ }),

/***/ "./src/js/models/node.js":
/*!*******************************!*\
  !*** ./src/js/models/node.js ***!
  \*******************************/
/*! exports provided: Node, NodeCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Node", function() { return Node; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NodeCollection", function() { return NodeCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);



class Node extends backbone__WEBPACK_IMPORTED_MODULE_2__["Model"] {
  defaults() {
    return {
      title: '',
      parent_id: '',
      ctype: '',
      kvstore: '',
      selected: false,
      img_src: '',
      created_at: '',
      user_perms: {}
    };
  }

  initialize(parent_id) {}

  urlRoot() {
    return '/node/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      parent_id: this.get('parent_id'),
      title: this.get('title'),
      created_at: this.get('created_at')
    };
    return dict;
  }

  get url() {
    if (this.is_document()) {
      // this url corresponds to backend's 
      // reverse('core:document', args=(doc_id))
      // and is used to open admin/documet.html template.
      return this.get('document_url');
    } // this form of url is used for folder browsing via json requests.


    return `/#${this.get('id')}`;
  }

  full_title() {
    return this.get('title');
  }

  short_title(len) {
    let result,
        text = this.get('title');

    if (text && text.length > len) {
      result = `${text.substring(0, len)}...`;
    } else {
      result = text;
    }

    return result;
  }

  is_document() {
    if (this.get('ctype') == 'document') {
      return true;
    }

    return false;
  }

  is_folder() {
    if (this.get('ctype') == 'folder') {
      return true;
    }

    return false;
  }

  find_page_kvstore_for(key) {
    /**
    * Returns kvstore of the provided key in first page
    of corresponding document.
    In browser list mode (and in document viewer if no page is selected)
    it is metadata of the first page displayed.
    **/
    let pages, kvstore, first_page, index; // pages are relevant only of nodes which are Documents.

    if (this.is_folder()) {
      return undefined;
    }

    pages = this.get('pages');

    if (pages) {
      first_page = pages[0];
      kvstore = first_page.kvstore;

      if (kvstore) {
        index = underscore__WEBPACK_IMPORTED_MODULE_0__["default"].findIndex(kvstore, function (kv) {
          return kv.key == key;
        });

        if (index >= 0) {
          return kvstore[index];
        }
      }
    }

    return undefined;
  }

  get_page_value_for(key) {
    let page_kvstore;
    page_kvstore = this.find_page_kvstore_for(key);

    if (page_kvstore) {
      return page_kvstore.value;
    }

    return '';
  }

  get_page_virtual_value_for(key) {
    let page_kvstore;
    page_kvstore = this.find_page_kvstore_for(key);

    if (page_kvstore) {
      return page_kvstore.virtual_value;
    }

    return '';
  }

  is_readonly() {
    let user_perms = this.get('user_perms'),
        result;
    result = user_perms['read'];
    result = result && !user_perms['write'];
    result = result && !user_perms['delete'];
    result = result && !user_perms['change_perm'];
    result = result && !user_perms['take_ownership'];
    return result;
  }

}
class NodeCollection extends backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"] {
  get model() {
    return Node;
  }

  urlRoot() {
    return '/nodes/';
  }

  collection_post_action(url, options, extra_data) {
    let token, post_data, request;
    token = jquery__WEBPACK_IMPORTED_MODULE_1___default()("[name=csrfmiddlewaretoken]").val();
    post_data = this.models.map(function (models) {
      return models.attributes;
    });

    if (extra_data) {
      post_data = { ...post_data,
        ...extra_data
      };
    }

    jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajaxSetup({
      headers: {
        'X-CSRFToken': token
      }
    });
    request = jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajax({
      method: "POST",
      url: url,
      data: JSON.stringify(post_data),
      contentType: "application/json",
      dataType: 'json'
    });
    request.done(options['success']);
  }

  delete(options) {
    this.collection_post_action(this.urlRoot(), options);
  }

  cut(options) {
    this.collection_post_action('/cut-node/', options);
  }

  _paste(url, options, parent_id) {
    let token, request;
    token = jquery__WEBPACK_IMPORTED_MODULE_1___default()("[name=csrfmiddlewaretoken]").val();
    jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajaxSetup({
      headers: {
        'X-CSRFToken': token
      }
    });
    request = jquery__WEBPACK_IMPORTED_MODULE_1___default.a.ajax({
      method: "POST",
      url: url,
      data: JSON.stringify({
        'parent_id': parent_id
      }),
      contentType: "application/json",
      dataType: 'json'
    });
    request.done(options['success']);
  }

  paste(options, parent_id) {
    // pastes folder or document
    this._paste('/paste-node/', options, parent_id);
  }

  paste_pages(options, parent_id) {
    // pastes pages
    this._paste('/paste-pages/', options, parent_id);
  }

}

/***/ }),

/***/ "./src/js/models/page.js":
/*!*******************************!*\
  !*** ./src/js/models/page.js ***!
  \*******************************/
/*! exports provided: Page, PageCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Page", function() { return Page; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PageCollection", function() { return PageCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);



class Page extends backbone__WEBPACK_IMPORTED_MODULE_2__["Model"] {
  defaults() {
    return {
      number: ''
    };
  }

  initialize() {}

  urlRoot() {
    return '/page/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      number: this.get('number')
    };
    return dict;
  }

}
class PageCollection extends backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"] {
  get model() {
    return Page;
  }

  urlRoot() {
    return '/pages/';
  }

}

/***/ }),

/***/ "./src/js/models/permission.js":
/*!*************************************!*\
  !*** ./src/js/models/permission.js ***!
  \*************************************/
/*! exports provided: Permission */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Permission", function() { return Permission; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils */ "./src/js/utils.js");




let ALLOW = 'allow';
let DENY = 'deny'; // allowed access_item types

let ALLOWED_TYPES = [ALLOW, DENY];
class Permission extends backbone__WEBPACK_IMPORTED_MODULE_2__["Model"] {
  defaults() {
    return {
      id: '',
      name: '',
      // e.g. admin
      model: '',
      // e.g. user/group
      access_type: ALLOW,
      access_inherited: false,
      permissions: {
        read: false,
        write: false,
        delete: false,
        change_perm: false,
        take_ownership: false
      }
    };
  }

  set_perm(name, checked) {
    let permissions = this.get('permissions');
    permissions[name] = checked;
    this.set({
      'permissions': permissions
    });
  }

  get_perm(name) {
    let permissions = this.get('permissions');
    return permissions[name];
  }

  set_type(access_type) {
    this.set({
      'access_type': access_type
    });
  }

  static get CHPERM() {
    return 'change_perm';
  }

  static get OWN() {
    return 'take_ownership';
  }

  static get READ() {
    return 'read';
  }

  static get WRITE() {
    return 'write';
  }

  static get DEL() {
    return 'delete';
  }

  human_access_type() {
    return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["capitalize"])(this.get('access_type'));
  }

  human_perms() {
    let text, permissions;
    let ch;
    let own;
    let write;
    let read;
    let del;
    permissions = this.get('permissions');
    ch = permissions[Permission.CHPERM];
    own = permissions[Permission.OWN];
    write = permissions[Permission.WRITE];
    read = permissions[Permission.READ];
    del = permissions[Permission.DEL];

    if (ch && own && write && read && del) {
      text = 'Full Control';
    } else if (read && write && !ch && !own && !del) {
      text = 'Read & Write';
    } else if (read && !write && !ch && !own && !del) {
      text = 'Read';
    } else if (read && write && !ch && !own && del) {
      text = 'Read & Write & Delete';
    } else {
      text = 'User Defined';
    }

    return text;
  }

}

/***/ }),

/***/ "./src/js/models/rename.js":
/*!*********************************!*\
  !*** ./src/js/models/rename.js ***!
  \*********************************/
/*! exports provided: Rename */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Rename", function() { return Rename; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);


class Rename extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  /**
      Used to rename folder/document.
  */
  urlRoot() {
    return '/rename-node/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      title: this.get('title')
    };
    return dict;
  }

}

/***/ }),

/***/ "./src/js/models/thumbnail.js":
/*!************************************!*\
  !*** ./src/js/models/thumbnail.js ***!
  \************************************/
/*! exports provided: Thumbnail, ThumbnailCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Thumbnail", function() { return Thumbnail; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ThumbnailCollection", function() { return ThumbnailCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);



class Thumbnail extends backbone__WEBPACK_IMPORTED_MODULE_2__["Model"] {
  defaults() {
    return {
      number: ''
    };
  }

  initialize() {}

  urlRoot() {
    return '/page/';
  }

  toJSON() {
    let dict = {
      id: this.get('id'),
      number: this.get('number')
    };
    return dict;
  }

}
class ThumbnailCollection extends backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"] {
  get model() {
    return Thumbnail;
  }

}

/***/ }),

/***/ "./src/js/models/uploader.js":
/*!***********************************!*\
  !*** ./src/js/models/uploader.js ***!
  \***********************************/
/*! exports provided: UploaderItem, Uploader */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UploaderItem", function() { return UploaderItem; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "Uploader", function() { return Uploader; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _utils__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../utils */ "./src/js/utils.js");




class UploaderItem extends backbone__WEBPACK_IMPORTED_MODULE_1__["Model"] {
  defaults() {
    return {
      title: '',
      size: '',
      file: '',
      lang: '',
      status: '',
      file_type: '',
      parent_id: -1,
      progress: 0
    };
  }

  initialize(file, lang, parent_id) {
    if (!parent_id) {
      parent_id = -1;
    }

    this.set({
      'title': file.name,
      'size': file.size,
      'file': file,
      'lang': lang,
      'file_type': file.type,
      'progress': 0,
      'parent_id': parent_id,
      'status': UploaderItem.INIT
    }); // once uploader item instance is created
    // immediately start upload process.

    this.send();
  }

  static get INIT() {
    // this is initial state
    // before uploading starts
    return "init";
  }

  static get UPLOAD_START() {
    return "upload_start";
  }

  static get UPLOAD_ERROR() {
    return "upload_error";
  }

  static get UPLOAD_SUCCESS() {
    return "upload_success";
  }

  static get UPLOAD_PROGRESS() {
    return "upload_progress";
  }

  is_success() {
    return this.get('status') == UploaderItem.UPLOAD_SUCCESS;
  }

  is_error() {
    return this.get('status') == UploaderItem.UPLOAD_ERROR;
  }

  is_progress() {
    return this.get('status') == UploaderItem.UPLOAD_PROGRESS;
  }

  get human_size() {
    return Object(_utils__WEBPACK_IMPORTED_MODULE_3__["human_size"])(this.get('size'));
  }

  set_progress(percent) {
    // percentage = (0..100), as integer
    this.set('progress', percent);
    this.trigger('change');
  }

  _build_form_data() {
    let form_data;
    form_data = new FormData();
    form_data.append("language", this.get('lang'));
    form_data.append("file_name", this.get("file_name"));
    form_data.append("file_type", this.get("file_type"));
    form_data.append("parent", this.get("parent_id"));
    form_data.append("file", this.get("file"));
    return form_data;
  }

  send() {
    /*
    This model class does NOT use Backbone's sync. The
    reason is that we need to closely monitor the progress of file uploads.
     */
    let xhr,
        percent,
        token,
        that = this;
    xhr = new XMLHttpRequest();
    xhr.addEventListener('progress', function (e) {
      if (e.lengthComputable) {
        percent = Math.round(e.loaded * 100 / e.total); // notify subscribers of "upload_progress" event

        that.set_progress(percent);
      }
    });

    function transferFailed(e) {
      console.log(`Transfer failed for ${that.get('title')}`);
      that.set({
        'status': UploaderItem.UPLOAD_ERROR
      });
    }

    function transferComplete(e) {
      console.log(`Complete? status = ${e.currentTarget.status}`);

      if (e.currentTarget.status == 200) {
        that.set({
          'status': UploaderItem.UPLOAD_SUCCESS
        });
      } else if (e.currentTarget.status == 500) {
        that.set({
          'status': UploaderItem.UPLOAD_ERROR
        });
      } else if (e.currentTarget.status == 400) {
        that.set({
          'status': UploaderItem.UPLOAD_ERROR
        });
      }
    }

    xhr.addEventListener("error", transferFailed);
    xhr.addEventListener("load", transferComplete);
    token = jquery__WEBPACK_IMPORTED_MODULE_2___default()("[name=csrfmiddlewaretoken]").val();
    xhr.open("POST", "/upload/");
    xhr.setRequestHeader("X-CSRFToken", token);
    xhr.send(this._build_form_data());
  } // send


}
class Uploader extends backbone__WEBPACK_IMPORTED_MODULE_1__["Collection"] {
  get model() {
    return UploaderItem;
  }

  get progress() {
    let total_progress = 0;
    this.each(function (it) {
      total_progress += it.get('progress');
    });

    if (this.length > 0) {
      total_progress = total_progress / this.length;
    }

    return total_progress;
  }

  get_summary_status() {
    let summary_status = {
      'success': 0,
      'error': 0
    };
    this.each(function (it) {
      if (it.is_success()) {
        summary_status['success'] += 1;
      }

      if (it.is_error()) {
        summary_status['error'] += 1;
      }
    });
    return summary_status;
  }

  is_summary_success() {
    let summary_status = this.get_summary_status();
    return summary_status['success'] == this.length;
  }

  is_summary_error() {
    let summary_status = this.get_summary_status();
    return summary_status['error'] > 0;
  }

}

/***/ }),

/***/ "./src/js/models/user_group.js":
/*!*************************************!*\
  !*** ./src/js/models/user_group.js ***!
  \*************************************/
/*! exports provided: UserGroup, UserGroupCollection */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserGroup", function() { return UserGroup; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UserGroupCollection", function() { return UserGroupCollection; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);



class UserGroup extends backbone__WEBPACK_IMPORTED_MODULE_2__["Model"] {}
class UserGroupCollection extends backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"] {
  url() {
    return '/usergroups';
  }

  get model() {
    return UserGroup;
  }

  parse(response, options) {
    let usergroups = response.usergroups,
        that = this; // do not trigger reset event

    that.reset([], {
      'silent': true
    });

    underscore__WEBPACK_IMPORTED_MODULE_0__["default"].each(usergroups, function (item) {
      that.add(new UserGroup(item));
    });

    this.trigger('change');
  }

}

/***/ }),

/***/ "./src/js/node.js":
/*!************************!*\
  !*** ./src/js/node.js ***!
  \************************/
/*! exports provided: get_current_parent_id, DgNode, DgFolder, DgDocument */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "get_current_parent_id", function() { return get_current_parent_id; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgNode", function() { return DgNode; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgFolder", function() { return DgFolder; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgDocument", function() { return DgDocument; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);

function get_current_parent_id() {
  // the root folder id, where we are now.
  return jquery__WEBPACK_IMPORTED_MODULE_0___default()("input#current_parent_id").val();
}
class DgNode {
  /*
    DgNode an abstraction of both Folder and Document DOM element in changelist view.
    
    Do not confuse it with DOM's node - concepts are completely unrelated.
    Also DgNode has nothing to do with node js. Well, maybe latter
    it will be moved as nodejs package.
  */
  constructor(id, title, dom_elem = undefined) {
    this._id = id;
    this._title = title;
    this._dom_elem = dom_elem;
  }

  static get selector() {
    // A DgNode is any dom element which
    // matches li.node selector.
    return "li.node";
  }

  addClass(cls) {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._dom_elem).addClass(cls);
  }

  get id() {
    return this._id;
  }

  get title() {
    return this._title;
  }

  get dom_elem() {
    return this._dom_elem;
  }

  static create_from_dom(dom_elem) {
    let title = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").text();
    let id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").data("id");
    return new DgNode(title, id, dom_elem);
  }

}
class DgFolder extends DgNode {
  static get selector() {
    // DgFolder is data abstraction of 
    // DOM elements this selector
    return "li.node.folder";
  }

  static create_from_dom(dom_elem) {
    /*
      A document node has its title in alt attribute of the
      anchor. Reason behind it is that text part of the
      anchor i.e. <a class="title">this is text part</a>
      can be truncated. As I said above the original 
      title is preserved in the alt attribute.
      Example:
       <a data-id="347" alt="Very Very Very Long Title.pdf">
        Very very very Lo...
      </a>
    */
    let title = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").attr("alt");
    let id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").data("id");
    return new DgFolder(id, title, dom_elem);
  }

}
class DgDocument extends DgNode {
  static get selector() {
    // DgDocument is data abstraction of 
    // DOM elements this selector
    return "li.node.document";
  }

  static create_from_dom(dom_elem) {
    /*
      A document node has its title in alt attribute of the
      anchor. Reason behind it is that text part of the
      anchor i.e. <a class="title">this is text part</a>
      can be truncated. As I said above the original 
      title is preserved in the alt attribute.
      Example:
       <a data-id="347" alt="Very Very Very Long Title.pdf">
        Very very very Lo...
      </a>
    */
    let title = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").attr('alt');
    let id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(dom_elem).find(".title > a").data("id");
    return new DgDocument(id, title, dom_elem);
  }

}

/***/ }),

/***/ "./src/js/routers/browse.js":
/*!**********************************!*\
  !*** ./src/js/routers/browse.js ***!
  \**********************************/
/*! exports provided: BrowseRouter */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BrowseRouter", function() { return BrowseRouter; });
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");




class BrowseRouter extends backbone__WEBPACK_IMPORTED_MODULE_2__["Router"] {
  constructor(browse_view, breadcrumb_view, actions_view) {
    super();
    this.browse_view = browse_view;
    this.breadcrumb_view = breadcrumb_view;
    this.actions_view = actions_view;
  }

  preinitialize() {
    let that = this;
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["PARENT_CHANGED"], function (parent_id) {
      if (parent_id) {
        that.navigate(`/${parent_id}`, {
          trigger: true
        });
      }
    });
  }

  routes() {
    return {
      ":node_id": "browse",
      "*path": "browse"
    };
  }

  browse(node_id) {
    /**
        There are multiple server side 'index.html' views. Each one with
        different root folder.
        E.g. browse => browse top level documents & folders.
             Inbox => browse documents in special Inbox folder.
         Both are served with same index.html file but with different
        django view function.
        In case of special folder - inbox - while index.html template is served
        an html div#root_node_id is initialized to signal router that root folder
        in this case is the one specified with $("#root_node_id").val();
         This solutions ensures clean implementation of another feature: highlight
        of active link on the right panel (when user clicks inbox -> highlight inbox,
        when user clicks documents -> highlight documents. Same for user and groups links).
    ***/
    if (!node_id) {
      if (jquery__WEBPACK_IMPORTED_MODULE_1___default()("#root_node_id").length > 0) {
        node_id = jquery__WEBPACK_IMPORTED_MODULE_1___default()("#root_node_id").val();
      }

      ;
    }

    this.browse_view.open(node_id);
    this.breadcrumb_view.open(node_id);
    this.actions_view.set_parent(node_id);
  }

}

/***/ }),

/***/ "./src/js/sort_cookie.js":
/*!*******************************!*\
  !*** ./src/js/sort_cookie.js ***!
  \*******************************/
/*! exports provided: sort_cookie */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "sort_cookie", function() { return sort_cookie; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);


function set_cookie(name, value, days) {
  console.log(`setting cookie named ${name} with value ${value}`);
  var expires = "";

  if (days) {
    var date = new Date();
    date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
    expires = "; expires=" + date.toUTCString();
  }

  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function sort_cookie() {
  /**
      This function resolves the ticket #15.
      Automatically sort by alphabet - feature request...
       The 'automatic sort' is accomplished with help of cookie.
      A cookie file is saved every time user clicks on:
          title asc/desc -> 1 / -1
          date asc/desc  -> 2 / -2
          type asc/desc  -> 3 / -3 
      sorting. 
      Cookie file name is 'save_last_sort' and it contains the corresponding
      number of the sort user chose (1, -1 etc).
      In changelist of basetreenode (on the server side), this cookie will
      be read in basetreenodes will be sorted accordingly. This so called
      cookie based sorting has lower precedence than 'o' parameter.
  **/
  jquery__WEBPACK_IMPORTED_MODULE_0___default()(".dropdown-item.sort").on('click', function () {
    let _$this = jquery__WEBPACK_IMPORTED_MODULE_0___default()(this);

    let value;

    if (_$this.hasClass("title") && _$this.hasClass("asc")) {
      value = 1;
    } else if (_$this.hasClass("title") && _$this.hasClass("desc")) {
      value = -1;
    } else if (_$this.hasClass("date") && _$this.hasClass("asc")) {
      value = 2;
    } else if (_$this.hasClass("date") && _$this.hasClass("desc")) {
      value = -2;
    } else if (_$this.hasClass("type") && _$this.hasClass("asc")) {
      value = 3;
    } else if (_$this.hasClass("type") && _$this.hasClass("desc")) {
      value = -3;
    }

    set_cookie("save_last_sort", value, 365);
  });
}

/***/ }),

/***/ "./src/js/spinner.js":
/*!***************************!*\
  !*** ./src/js/spinner.js ***!
  \***************************/
/*! exports provided: DgMainSpinner */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgMainSpinner", function() { return DgMainSpinner; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);

class DgMainSpinner {
  constructor(spinner_id = "#preload-spinner", container_id = "#viewer") {
    let that = this;
    this._spinner_id = spinner_id;
    this._container_id = container_id;
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(window).on("load", function () {
      console.log("document form load complete");
      that.show();
    });
  }

  hide() {
    // hide whole body > main container
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._spinner_id).addClass("invisible");
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._container_id).addClass("invisible");
  }

  show() {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._container_id).removeClass("invisible");
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._spinner_id).removeClass("invisible");
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(this._spinner_id).hide();
  }

}

/***/ }),

/***/ "./src/js/templates/access.html":
/*!**************************************!*\
  !*** ./src/js/templates/access.html ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div class="modal-dialog modal-lg modal-dialog-centered" role="document">\n    <div class="modal-content">\n        <div class="modal-header">\n            <h5 class="modal-title">'+
((__t=( gettext('Access') ))==null?'':__t)+
' ('+
((__t=( node.get('title') ))==null?'':__t)+
')</h1>\n            <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n              <span aria-hidden="true">&times;</span>\n            </button>\n        </div>\n        <div class="modal-body">\n            <ul id="permission_actions" class="nav nav-pills">\n                <li class="mx-1">\n                    <button id="create_perm" class="btn btn-light btn-bordered">\n                        <i class="fa fa-plus mr-1 text-success"></i>'+
((__t=( gettext('Create') ))==null?'':__t)+
'\n                    </button>\n                </li>\n                <li class="mx-1">\n                    <button id="edit_perm" class="btn btn-light btn-bordered">\n                        <i class="fa fa-edit mr-1 text-success"></i>'+
((__t=( gettext('Edit') ))==null?'':__t)+
'\n                    </button>\n                </li>\n                <li class="mx-1">\n                    <button id="delete_perm" class="btn btn-light btn-bordered">\n                        <i class="fa fa-times mr-1 text-danger"></i>'+
((__t=( gettext('Delete') ))==null?'':__t)+
'\n                    </button>\n                </li>\n                <li class="mx-1">\n                    <button id="readonly_view_perm" class="btn btn-light btn-bordered">\n                         <i class="fa fa-eye mr-1 text-success"></i>'+
((__t=( gettext('View') ))==null?'':__t)+
'\n                    </button>\n                </li>\n            </ul>\n            <table class="table table-striped">\n                <thead class="thead-light">\n                    <tr>\n                        <td>\n                            '+
((__t=( gettext('User or Group') ))==null?'':__t)+
'\n                        </td>\n                        <td>\n                            '+
((__t=( gettext('Type') ))==null?'':__t)+
'\n                        </td>\n                        <td>\n                            '+
((__t=( gettext('Access') ))==null?'':__t)+
'\n                        </td>\n                    </tr>\n                </thead> <!--- header -->\n                <tbody id="access_items">\n                    ';
 for (i=0; i < acc_collection.models.length; i++) { 
__p+='\n                        ';
 item = acc_collection.models[i]; 
__p+='\n                        <tr class="';
 if (item.get('access_inherited')) {  
__p+='disabled';
 } 
__p+='" data-cid="'+
((__t=( item.cid  ))==null?'':__t)+
'" data-model="'+
((__t=( item.get('model')  ))==null?'':__t)+
'"  data-name="'+
((__t=( item.get('name')  ))==null?'':__t)+
'" data-id="'+
((__t=( item.get('id')  ))==null?'':__t)+
'">\n                            <td>'+
((__t=( item.get('name') ))==null?'':__t)+
'</td>\n                            <td>'+
((__t=( gettext(item.human_access_type()) ))==null?'':__t)+
'</td>\n                            <td>'+
((__t=( gettext(item.human_perms()) ))==null?'':__t)+
'</td>\n                        </tr>\n                    ';
 } 
__p+='\n                </tbody> <!-- end of body -->\n            </table> <!--  table -->\n        </div>\n        <div class="modal-footer">\n            <button type="submit" class="btn btn-success action margin-xs apply">\n                '+
((__t=( gettext('Apply') ))==null?'':__t)+
'\n            </button>\n            <button data-dismiss="modal" class="btn margin-xs btn-secondary cancel">\n                '+
((__t=( gettext('Cancel') ))==null?'':__t)+
'\n            </button></a>\n        </div>\n    </div> <!-- modal content -->\n</div>';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/breadcrumb.html":
/*!******************************************!*\
  !*** ./src/js/templates/breadcrumb.html ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<ol class="breadcrumb float-sm-left">\n    <li class="breadcrumb-item">\n        <a href="/"><i class="fa fa-home px-1"></i>'+
((__t=( gettext('Home') ))==null?'':__t)+
'</a>\n    </li>\n    ';
 for (i=0; i < nodes.length; i++) { 
__p+='\n        ';
 node = nodes.at(i) 
__p+='\n        <li class="breadcrumb-item">\n            <a href="'+
((__t=( node.url ))==null?'':__t)+
'" class="breadcrumb-node"  data-id="'+
((__t=( node.get('id') ))==null?'':__t)+
'">\n            	'+
((__t=( node.get('title') ))==null?'':__t)+
'\n            </a>\n        </li>\n    ';
 } 
__p+='\n</ol>\n';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/browse_grid.html":
/*!*******************************************!*\
  !*** ./src/js/templates/browse_grid.html ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<ul class="d-flex grid">\n    ';
 for (i=0; i < nodes.length; i++) { 
__p+='\n        ';
 node = nodes.at(i) 
__p+='\n        <li class="node node-w1 d-flex flex-column align-items-center" data-id="'+
((__t=( node.get('id') ))==null?'':__t)+
'" data-cid="'+
((__t=( node.cid ))==null?'':__t)+
'" data-url="'+
((__t=( node.url ))==null?'':__t)+
'">\n            ';
 if (node.is_document())  { 
__p+='\n                <div class="placeholder document">\n                    <img class="zero_pix" src="'+
((__t=(  node.get('img_src') ))==null?'':__t)+
'" />\n                    <div class="document-loading"></div>\n                </div>\n            ';
 } 
__p+='\n            <div class="icon-'+
((__t=( node.get('ctype') ))==null?'':__t)+
'">\n            </div>\n            <div class="icons">\n                ';
 if (node.is_readonly()) {  
__p+='\n                    <i class="fa fa-lock"></i>\n                ';
 } 
__p+='\n            </div>\n            <input type="checkbox" name="_selected_action" value="'+
((__t=( node.get('id') ))==null?'':__t)+
'" class="action-select" />\n            <div class="title tooltip">\n                <a href="#" class="'+
((__t=( node.get('ctype') ))==null?'':__t)+
'" data-id="'+
((__t=( node.get('id') ))==null?'':__t)+
'" alt="'+
((__t=(  node.full_title() ))==null?'':__t)+
'">'+
((__t=( node.short_title(20) ))==null?'':__t)+
'</a>\n                <span class="tooltiptext">'+
((__t=( node.full_title()  ))==null?'':__t)+
'</span>\n            </div>\n        </li>\n    ';
 } 
__p+='\n</ul>';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/browse_list.html":
/*!*******************************************!*\
  !*** ./src/js/templates/browse_list.html ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<table class="table">\n  <thead>\n    <tr>\n      <th scope="col">\n        <a \n          href="#"\n          class="header sort d-flex justify-content-between align-items-center"\n          data-col="type"\n        >\n          '+
((__t=( gettext('Type') ))==null?'':__t)+
'\n          <i class="fa '+
((__t=( table.cols[0].sort_icon_name ))==null?'':__t)+
'"></i>\n        </a>\n      </th>\n      <th scope="col">\n        <a\n          href="#"\n          class="header sort d-flex justify-content-between align-items-center"\n          data-col="title"\n        >\n          '+
((__t=( gettext('Title ') ))==null?'':__t)+
'\n          <i class="fa '+
((__t=( table.cols[1].sort_icon_name ))==null?'':__t)+
'"></i>\n        </a>\n      </th>\n      ';
 for (i=0; i < table.key_cols.length; i++) { 
__p+='\n        ';
 column = table.key_cols[i] 
__p+='\n        ';
 if (column) { 
__p+='\n          <th scope="col">\n            <a \n              href="#"\n              class="header sort d-flex justify-content-between align-items-center"\n              data-col="key" data-key="'+
((__t=( column.key ))==null?'':__t)+
'"\n            >\n              '+
((__t=( column.key ))==null?'':__t)+
'\n              <i class="fa '+
((__t=( column.sort_icon_name ))==null?'':__t)+
'"></i>\n            </a>\n          </th>\n        ';
 } 
__p+='\n      ';
 } 
__p+='\n      <th scope="col">\n        <a\n          href="#"\n          class="header sort d-flex justify-content-between align-items-center"\n          data-col="created_at"\n        >\n          '+
((__t=( gettext('Created At') ))==null?'':__t)+
'\n          <i class="fa  '+
((__t=( table.cols[table.cols.length -1].sort_icon_name ))==null?'':__t)+
'"></i>\n        </a>\n      </th>\n    </tr>\n  </thead>\n  <tbody>\n    ';
 for (i=0; i < table.rows.length; i++) { 
__p+='\n        ';
 row = table.rows[i] 
__p+='\n    <tr class="node" data-id="'+
((__t=( row[0].id ))==null?'':__t)+
'" data-cid="'+
((__t=( row[0].cid ))==null?'':__t)+
'" data-url="'+
((__t=( row[0].url ))==null?'':__t)+
'">\n        ';
 for (j=0; j < row.length; j++) { 
__p+='\n          <td>'+
((__t=( row[j].value ))==null?'':__t)+
'</td>\n        ';
 } 
__p+='\n    </tr>\n    ';
 } 
__p+='\n  </tbody>\n</table>';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/display_mode.html":
/*!********************************************!*\
  !*** ./src/js/templates/display_mode.html ***!
  \********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div class="dropdown">\n    <button class="btn btn-light dropdown-toggle" type="button" id="dropdown_view_opt" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">\n      ';
 if (is_list) { 
__p+='\n        <i class="fa fa-bars"></i>\n      ';
 } else { 
__p+='\n        <i class="fa fa-th"></i>\n      ';
 } 
__p+='\n    </button>\n    <div class="dropdown-menu dropdown-menu-right" aria-labelledby="dropdownMenuButton">\n        <a href="#" class="dropdown-item display-grid">\n          <i class="fa fa-th"> </i><span class="px-2">Grid</span>\n          ';
 if (is_grid) { 
__p+='\n            <i class="fa fa-check text-green"></i>\n          ';
 } 
__p+='\n        </a>\n        <a href="#" class="dropdown-item display-list"><i class="fa fa-bars"></i>\n          <span class="px-2">List</span>\n          ';
 if (is_list) { 
__p+='\n            <i class="fa fa-check text-green"></i>\n          ';
 } 
__p+='\n      </a>\n    </div>\n</div>\n\n<div class="dropdown order">\n    <button class="btn btn-light dropdown-toggle" type="button" id="dropdown_order_opt" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">\n      <i class="fa fa-sort-amount-up"></i>\n    </button>\n    <ul class="dropdown-menu dropdown-menu-right sort" aria-labelledby="navbarDropdownMenuLink">\n          <li class="dropdown-submenu-left dropdown-submenu">\n            <a class="dropdown-item dropdown-toggle" href="#">Title</a>\n            <ul class="dropdown-menu">\n              <li><a class="dropdown-item sort asc title" href="/admin/core/basetreenode/?o=1">\n                Asc\n              </a></li>\n              <li><a class="dropdown-item sort desc title" href="/admin/core/basetreenode/?o=-1">\n                Desc\n              </a></li>\n            </ul>\n          </li>\n          <li class="dropdown-submenu dropdown-submenu-left"><a class="dropdown-item dropdown-toggle" href="#">\n            Date\n          </a>\n            <ul class="dropdown-menu">\n              <li><a class="dropdown-item sort asc date" href="/admin/core/basetreenode/?o=2">\n                Asc\n              </a></li>\n              <li><a class="dropdown-item sort desc date" href="/admin/core/basetreenode/?o=-2">\n                Desc\n            </a></li>\n            </ul>\n          </li>\n          <li class="dropdown-submenu-left dropdown-submenu"><a class="dropdown-item dropdown-toggle" href="#">\n            Type\n          </a>\n            <ul class="dropdown-menu">\n              <li><a class="dropdown-item sort asc type" href="/admin/core/basetreenode/?o=3">\n                Asc\n              </a></li>\n              <li><a class="dropdown-item sort desc type" href="/admin/core/basetreenode/?o=-3">\n                Desc\n              </a></li>\n            </ul>\n          </li>\n        </ul>\n    </div>';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/metadata.html":
/*!****************************************!*\
  !*** ./src/js/templates/metadata.html ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+=' <h5 class="border-bottom">\n    '+
((__t=( gettext('Metadata') ))==null?'':__t)+
'\n</h5>\n <ul>\n    <li>\n        <button id="add_simple_meta" class="btn btn-success btn-sm btn-flat" type="button" ><i class="fa fa-plus"></i></button>\n    </li>\n </ul>\n <ul id="simple_keys" class="vertical menu">\n    ';
 for (i=0; i < kvstore.models.length; i++) { 
__p+='\n        ';
 item = kvstore.models[i]; 
__p+='\n        ';
 current_formats = item.get('current_formats') || []; 
__p+='\n        ';
 kv_types = item.get('kv_types') || available_types || []; 
__p+='\n        <li class=\'container\' data-model=\'simple-key\' data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\' data-value="'+
((__t=( item.get('key') ))==null?'':__t)+
'">\n            <div class="row summary">\n                <div class="col-11 label">\n                    <input '+
((__t=( item.disabled ))==null?'':__t)+
' data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\' placeholder="label name..." name=\'key\' type=\'text\' value="'+
((__t=( item.get('key') ))==null?'':__t)+
'">\n                </div>\n                <div class="col-1 close"  data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\'>\n                    ';
 if (!item.get('kv_inherited')) {  
__p+='\n                        <button type=\'button\' class=\'close key text-white mx-1\' aria-label=\'Close\'>\n                            <span aria-hidden=\'true\'>&times;</span>\n                        </button>\n                    ';
 } 
__p+='\n                </div>\n            </div>\n            <div class="row">\n                <div class="col-4">\n                    <label>Type</label>\n                </div>\n                <div class="col-8">\n                    <select '+
((__t=( item.disabled ))==null?'':__t)+
'  class="kv_type" name=\'kv_type\' class="custom-select">\n                        ';
 for (k=0; k < kv_types.length; k++) { 
__p+='\n                            <option \n                                ';
 if ( item.get('kv_type') == kv_types[k][0] ) { 
__p+=' selected  ';
 }  
__p+=' \n                                value="'+
((__t=( kv_types[k][0] ))==null?'':__t)+
'">\n                                '+
((__t=( kv_types[k][1] ))==null?'':__t)+
'\n                            </option>\n                        ';
 } 
__p+='\n                    </select>\n                </div>\n            </div>\n            <div class="row">\n                <div class="col-4">\n                    <label>Format</label>\n                </div>\n                <div class="col-8">\n                    <select '+
((__t=( item.disabled ))==null?'':__t)+
' class="kv_format" name=\'kv_format\' class="custom-select">\n                        ';
 for (j=0; j < current_formats.length; j++) { 
__p+='\n                            <option \n                                 ';
 if ( item.get('kv_format') == current_formats[j][0] ) { 
__p+=' selected  ';
 }  
__p+=' \n                                value="'+
((__t=( current_formats[j][0] ))==null?'':__t)+
'">\n                                '+
((__t=( current_formats[j][1] ))==null?'':__t)+
'\n                                \n                            </option>\n                        ';
 } 
__p+='\n                    </select>\n                </div>\n            </div>\n           \n        </li>\n    ';
 } 
__p+='\n </ul>\n ';
 if (kvstore.models.length > 0 && !all_disabled) { 
__p+='\n     <button type=\'button\' class=\'btn btn-success btn-flat save key mx-1\'>\n         Save\n     </button>\n ';
 } 
__p+='\n';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/metadata_page.html":
/*!*********************************************!*\
  !*** ./src/js/templates/metadata_page.html ***!
  \*********************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+=' <h5 class="border-bottom">Metadata</h5>\n <ul>\n    <li>\n        <button id="add_simple_meta" class="btn btn-success btn-sm btn-flat" type="button" ><i class="fa fa-plus"></i></button>\n    </li>\n </ul>\n <ul id="simple_keys" class="vertical menu">\n    ';
 for (i=0; i < kvstore.models.length; i++) { 
__p+='\n        ';
 item = kvstore.models[i]; 
__p+='\n        ';
 current_formats = item.get('current_formats') || []; 
__p+='\n        ';
 kv_types = item.get('kv_types') || available_types || []; 
__p+='\n        <li class=\'container\' data-model=\'simple-key\' data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\' data-value="'+
((__t=( item.get('key') ))==null?'':__t)+
'">\n            <div class="row summary">\n                <div class="col-11 label">\n                    <input '+
((__t=( item.disabled ))==null?'':__t)+
' data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\' placeholder="label name..." name=\'key\' type=\'text\' value="'+
((__t=( item.get('key') ))==null?'':__t)+
'">\n                </div>\n                <div class="col-1 close"  data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\'>\n                    ';
 if (!item.get('kv_inherited')) {  
__p+='\n                        <button type=\'button\' class=\'close key text-white mx-1\' aria-label=\'Close\'>\n                            <span aria-hidden=\'true\'>&times;</span>\n                        </button>\n                    ';
 } 
__p+='\n                </div>\n            </div> <!-- row.summary -->\n            <div class="row summary align-items-center">\n                <div class="col-11 label">\n                    <input data-id=\''+
((__t=( item.id ))==null?'':__t)+
'\' data-cid=\''+
((__t=( item.cid ))==null?'':__t)+
'\' placeholder="value..." name=\'value\' type=\'text\' value="'+
((__t=( item.get('value') ))==null?'':__t)+
'">\n                </div>\n                <div class="col-1 chevron toggle d-flex">\n                    <a class="m-1" href="#">\n                        <i class="fa fa-chevron-left"></i>\n                    </a>\n                </div>\n            </div> <!-- row.summary -->\n            <div class="row details d-none">\n                <div class="col-4">\n                    <label>Type</label>\n                </div>\n                <div class="col-8">\n                    ';
 if (item.disabled) { 
__p+='\n                        <label>'+
((__t=( item.get('kv_type') ))==null?'':__t)+
'</label>\n                    ';
 } else { 
__p+='\n                        <select class="kv_type" name=\'kv_type\' class="custom-select">\n                            ';
 for (k=0; k < kv_types.length; k++) { 
__p+='\n                                <option \n                                    ';
 if ( item.get('kv_type') == kv_types[k][0] ) { 
__p+=' selected  ';
 }  
__p+=' \n                                    value="'+
((__t=( kv_types[k][0] ))==null?'':__t)+
'">\n                                    '+
((__t=( kv_types[k][1] ))==null?'':__t)+
'\n                                </option>\n                            ';
 } 
__p+='\n                        </select>\n                    ';
 } 
__p+='\n                </div>\n            </div>\n            <div class="row details d-none">\n                <div class="col-4">\n                    <label>Format</label>\n                </div>\n                <div class="col-8">\n                    ';
 if (item.disabled) { 
__p+='\n                        <label>'+
((__t=( item.get('kv_format') || 'Free form' ))==null?'':__t)+
'</label>\n                    ';
 } else { 
__p+='\n                        <select class="kv_format" name=\'kv_format\' class="custom-select">\n                            ';
 for (j=0; j < current_formats.length; j++) { 
__p+='\n                                <option \n                                     ';
 if ( item.get('kv_format') == current_formats[j][0] ) { 
__p+=' selected  ';
 }  
__p+=' \n                                    value="'+
((__t=( current_formats[j][0] ))==null?'':__t)+
'">\n                                    '+
((__t=( current_formats[j][1] ))==null?'':__t)+
'\n                                </option>\n                            ';
 } 
__p+='\n                        </select>\n                    ';
 } 
__p+='\n                </div>\n            </div>\n           \n        </li>\n    ';
 } 
__p+='\n </ul>\n <button id="save-metadata" type=\'hidden\' class=\'btn btn-success btn-flat save key mx-1\'>\n     Save\n </button>\n';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/new_folder.html":
/*!******************************************!*\
  !*** ./src/js/templates/new_folder.html ***!
  \******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div class="modal-dialog modal-dialog-centered" role="document">\n  <div class="modal-content">\n    <div class="modal-header">\n      <h5 class="modal-title">\n          Create Folder\n      </h5>\n      <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n        <span aria-hidden="true">&times;</span>\n      </button>\n    </div>\n      <div class="modal-body">\n            <div class="modal-body vertical">\n              <form id="new-folder-form" method="POST">\n                  <div class="form-group">\n                    <label for="title">Folder name:</label>\n                    <input type="text" class="form-control" id="title" name="title">\n                    <input name="parent_id" value="" type="hidden" >\n                  </div>\n              </form>\n            </div>\n      </div>\n      <div class="modal-footer">\n            <button type="submit" class="btn btn-success action margin-xs create" >Create</button>\n            <button data-dismiss="modal" class="btn margin-xs btn-secondary cancel">Cancel</button></a>\n      </div>\n  </div>\n</div>\n';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/permission_editor.html":
/*!*************************************************!*\
  !*** ./src/js/templates/permission_editor.html ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div class="modal-dialog modal-dialog-centered" role="document">    <div class="modal-content">\n        <div class="modal-header">\n            <h5>'+
((__t=( gettext('Permission Editor') ))==null?'':__t)+
'</h5>\n            <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n              <span aria-hidden="true">&times;</span>\n            </button>\n        </div>\n        <div class="modal-body">\n            <div class="form-group">\n                <label class="padding-x-xs">'+
((__t=( gettext('User or Group') ))==null?'':__t)+
':</label>\n                <select ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="perm_user_or_group form-control" multiple title="'+
((__t=( gettext('Nothing selected') ))==null?'':__t)+
'">\n                    ';
 for (i=0; i < usergroups.models.length; i++) { 
__p+='\n                        ';
 item = usergroups.models[i]; 
__p+='\n                        <option ';
 if (item.get('name') == permission.get('name') && item.get('model') == permission.get('model')) { 
__p+=' selected ';
 } 
__p+=' data-model="'+
((__t=( item.get('model') ))==null?'':__t)+
'">\n                            '+
((__t=( item.get('name') ))==null?'':__t)+
'\n                        </option>\n                    ';
 } 
__p+='\n                </select>\n            </div>  \n            <div class="form-group">\n                <label class="padding-x-xs">'+
((__t=( gettext('Type') ))==null?'':__t)+
':</label>\n                <select ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' name="access_type" class="access_type">\n                    <option ';
 if ('allow' == permission.get('access_type')) { 
__p+=' selected ';
 } 
__p+=' value="allow">'+
((__t=( gettext('Allow') ))==null?'':__t)+
'</option>\n                    <option ';
 if ('deny' == permission.get('access_type')) { 
__p+=' selected ';
 } 
__p+='  value="deny">'+
((__t=( gettext('Deny') ))==null?'':__t)+
'</option>\n                </select>\n            </div>\n            <formset class="d-flex flex-column">\n                <div class="form-check">\n                    <input ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="margin-right-sm checkbox" type="checkbox" name="change_perm" ';
 if (permission.get_perm('change_perm')) { 
__p+=' checked ';
 } 
__p+=' >\n                    <label class="padding-x-xs horizonal">'+
((__t=( gettext('Change Permissions') ))==null?'':__t)+
'</label>\n                </div>\n                <div class="form-check">\n                    <input ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="margin-right-sm checkbox" type="checkbox" name="take_ownership" ';
 if (permission.get_perm('take_ownership')) { 
__p+=' checked ';
 } 
__p+=' >\n                    <label class="padding-x-xs horizonal">'+
((__t=( gettext('Take Ownership') ))==null?'':__t)+
'</label>\n                </div>\n                <div class="form-check">\n                    <input ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="margin-right-sm checkbox" type="checkbox" name="read"\n                    ';
 if (permission.get_perm('read')) { 
__p+=' checked ';
 } 
__p+='\n                    >\n                    <label class="padding-x-xs horizonal">'+
((__t=( gettext('Read') ))==null?'':__t)+
'</label>\n                </div>\n                <div class="form-check">\n                    <input ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="margin-right-sm checkbox" type="checkbox" name="write"\n                    ';
 if (permission.get_perm('write')) { 
__p+=' checked ';
 } 
__p+='\n                    >\n                    <label class="padding-x-xs horizonal">'+
((__t=( gettext('Write') ))==null?'':__t)+
'</label>\n                </div>\n                <div class="form-check">\n                    <input ';
 if (!edit) { 
__p+=' disabled ';
 } 
__p+=' class="margin-right-sm checkbox" type="checkbox" name="delete"\n                    ';
 if (permission.get_perm('delete')) { 
__p+=' checked ';
 } 
__p+='\n                    >\n                    <label class="padding-x-xs horizonal"> '+
((__t=( gettext('Delete') ))==null?'':__t)+
'</label>\n                </div>\n            </formset>\n        </div>\n        <div class="modal-footer">\n            <button type="submit" class="btn btn-success action margin-xs apply">\n                '+
((__t=( gettext('Apply') ))==null?'':__t)+
'\n            </button>\n            <button data-dismiss="modal" class="btn margin-xs btn-secondary cancel">\n                '+
((__t=( gettext('Cancel') ))==null?'':__t)+
'\n            </button></a>\n        </div>\n    </div> <!-- modal-content -->\n</div> <!-- modal-dialog -->';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/rename.html":
/*!**************************************!*\
  !*** ./src/js/templates/rename.html ***!
  \**************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div class="modal-dialog modal-dialog-centered" role="document">\n  <div class="modal-content">\n    <div class="modal-header">\n      <h5 class="modal-title">\n          '+
((__t=( gettext('Rename') ))==null?'':__t)+
'\n      </h5>\n      <button type="button" class="close" data-dismiss="modal" aria-label="Close">\n        <span aria-hidden="true">&times;</span>\n      </button>\n    </div>\n      <div class="modal-body">\n            <div class="modal-body vertical">\n              <form id="new-folder-form" method="POST">\n                  <div class="form-group">\n                    <label for="title">'+
((__t=( gettext('New Name') ))==null?'':__t)+
':</label>\n                    <input type="text" class="form-control" id="title" value="'+
((__t=( title ))==null?'':__t)+
'" name="title" />\n                  </div>\n              </form>\n            </div>\n      </div>\n      <div class="modal-footer">\n            <button type="submit" class="btn btn-success action margin-xs rename">'+
((__t=( gettext('Rename') ))==null?'':__t)+
'</button>\n            <button data-dismiss="modal" class="btn margin-xs btn-secondary cancel">'+
((__t=( gettext('Cancel') ))==null?'':__t)+
'</button></a>\n      </div>\n  </div>\n</div>';
}
return __p;
};


/***/ }),

/***/ "./src/js/templates/uploader.html":
/*!****************************************!*\
  !*** ./src/js/templates/uploader.html ***!
  \****************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = function(obj){
var __t,__p='',__j=Array.prototype.join,print=function(){__p+=__j.call(arguments,'');};
with(obj||{}){
__p+='<div id="upload_feedback" class="border-thin card">\n    <div class="card-header container-fluid" id="newsHeading">\n        <div class="row">\n            <div class="col">\n                ';
 if (files.is_summary_success()) { 
__p+='\n                    <h5 class="text-success">Done!</h5>\n                ';
 } else if (files.is_summary_error()) { 
__p+='\n                    <h5 class="text-danger">Error</h5>\n                ';
 } else { 
__p+='\n                    <h5>Uploading...</h5>\n                ';
 } 
__p+='\n            </div>\n            <div class="col">\n                <button type="button" class="close text-danger" aria-label="Close">\n                  <span aria-hidden="true">&times;</span>\n                </button>\n            </div>\n        </div>\n    <div class="hidden uploader-details">\n        <div class="details">\n            \n            ';
 for (i=0; i < files.length; i++) { 
__p+='\n                ';
 file = files.at(i) 
__p+='\n                <div style="background-size: '+
((__t=( file.get('progress') ))==null?'':__t)+
'% 100% %>" class="row ';
 if (file.is_error()) { 
__p+=' status-fail ';
 } else { 
__p+=' status-success ';
 } 
__p+='">\n                    <div class="col-1">\n                        <div class="status">\n                            ';
 if (file.is_error()) { 
__p+='\n                                <i class="fa fa-times text-danger"></i>\n                            ';
 } else if (file.is_success()) { 
__p+='\n                                <i class="fa fa-check-circle text-success"></i>\n                            ';
 } else if (file.is_progress()) { 
__p+='\n                                <i class="fa fa-spinner"></i>\n                            ';
 }  
__p+='\n                        </div>\n                    </div>\n                    <div class="col-7">\n                        <div class="filename">'+
((__t=( file.get('title') ))==null?'':__t)+
'</div>\n                    </div>\n                    <div class="col-2 text-right">\n                        <div class="size">'+
((__t=( file.human_size ))==null?'':__t)+
'</div>\n                    </div>\n                    <div class="col-2 text-right">\n                        <div class="lang">'+
((__t=( file.get('lang') ))==null?'':__t)+
'</div>\n                    </div>\n                </div>\n            ';
 } 
__p+='\n            \n        </div>\n    </div>\n    <div id="upload_feedback_summary">\n        <div class="row my-2 align-items-center">\n            <div id="uploader_short_status" class="col-4 status">\n                ';
 if (files.is_summary_success()) { 
__p+='\n                    <i class="fa fa-check-circle  text-success"></i>\n                ';
 } else { 
__p+='\n                    <i class="fa fa-times  text-danger"></i>\n                ';
  } 
__p+='\n            </div>\n            <div id="uploader_text_status" class="col-4 filename padding-left-md">\n            </div>\n            <div class="col-4 text-right">\n                <button class="btn btn-neuter btn-bordered toggle-details">\n                    Details\n                </button>\n            </div>\n        </div>\n    </div>\n    <div class="progress progress-bar-animated progress-sm active">\n        <div class="progress-bar ';
 if (files.is_summary_success()) { 
__p+='progress-bar-success ';
 } else { 
__p+=' progress-bar-fail ';
 } 
__p+='" role="progressbar" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100" style="width: '+
((__t=( files.progress ))==null?'':__t)+
'%">\n            <span class="sr-only">20% Complete</span>\n        </div>\n    </div>\n</div>';
}
return __p;
};


/***/ }),

/***/ "./src/js/text_overlay.js":
/*!********************************!*\
  !*** ./src/js/text_overlay.js ***!
  \********************************/
/*! exports provided: DgTextOverlay */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DgTextOverlay", function() { return DgTextOverlay; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);


Number.isNumeric = function (value) {
  return !isNaN(parseFloat(value)) && isFinite(value);
};

function build_svg(tag, attrs) {
  let el = document.createElementNS('http://www.w3.org/2000/svg', tag);

  for (var k in attrs) {
    el.setAttribute(k, attrs[k]);
  }

  return el;
}

class DgSVGText {
  constructor(x, y, text) {
    this.x = x;
    this.y = y;
    this.text = text;
  }

  make_svg() {
    let dom = build_svg('text', {
      'x': this.x,
      'y': this.y
    });
    let text_node = document.createTextNode(this.text);
    dom.appendChild(text_node);
    return dom;
  }

}

class DgBBox {
  constructor(x1, y1, x2, y2) {
    this.x1 = x1;
    this.y1 = y1;
    this.x2 = x2;
    this.y2 = y2;
  }

  get width() {
    return this.x2 - this.x1;
  }

  get height() {
    return this.y2 - this.y1;
  }

}

class DgTextOverlay {
  /*
      Creates an svg overlay for given image_id
  */
  constructor(dom_img, dom_parent, orig_img_rect) {
    /* Image width and height */
    let img_rect, height, width;
    img_rect = dom_img.getBoundingClientRect();
    this.height = img_rect.height;
    this.width = img_rect.width;
    this.dom_img = dom_img;
    this.dom_parent = dom_parent;
    this.orig_img_rect = orig_img_rect;
  }

  make_svg_container() {
    let dom = build_svg('svg', {
      'width': this.width,
      'height': this.height
    });
    return dom;
  }

  fit_text_to_bbox(dest_bbox, svg_item, dg_svg_text) {
    // http://kba.cloud/hocr-spec/1.2/#bbox
    let bb = svg_item.getBBox();
    let w, h, tx, ty, ratio;

    if (!this.orig_img_rect) {
      return;
    }

    ratio = parseInt(this.width) / this.orig_img_rect.width;

    if (Number.isNumeric(bb.width) && bb.width > 0) {
      /**
          w = (img_cur_w / img_orig_w) * (server_text_w / text_w)
           img_cur_w = img width from current DOM (adjusted to fit page width)
          img_orig_w = img original width
          server_text_w = text width as per HOCR data (retrieved from server)
          text_w = width of text as in current DOM: svg.getBBox()
           ISSUE: for some elements server_text_w (dest_bbox.width in code)
          is too large, i.e. it has width of whole page. This happens because
          HOCR data is wrong. Example: 
              <span class='ocrx_word' 
                      id='word_1_217' 
                      title='bbox 0 0 1240 1755; 
                      x_wconf 92'>:</span>
           In example above, as per server data, bbox's width (width of ":") will be
          1240 - 0 = 1240 which is obviously wrong.
           To avoid one bbox element covering whole page, below code will
          not scale all elemetns with where server_text_w / text_w > 20
      **/
      w = ratio * dest_bbox.width / bb.width;
    } else {
      return;
    }

    if (Number.isNumeric(bb.height) && bb.height > 0) {
      h = dest_bbox.height / bb.height;
    } else {
      return;
    }

    if (!Number.isNumeric(w)) {
      console.log(`[${dg_svg_text.text}] invalid scale value. dest_bbox.width = ${dest_bbox.width}; bb.width=${bb.width}; w=${w}`);
      return;
    }

    tx = ratio * dest_bbox.x1 / w;
    ty = ratio * dest_bbox.y2 / w; //  To avoid one bbox element covering whole page, below code will
    //  not scale all elemetns with where server_text_w / text_w > 20

    if (dest_bbox.width / bb.width <= 20) {
      svg_item.setAttribute("transform", "scale(" + w + ")");
      /*
      console.log(
          `OK w=${w}`
      );
      console.log(
          `OK width=${this.width} / orig_img_rect.width=${this.orig_img_rect.width}`
      );
      console.log(
           `OK dest_bbox.width=${dest_bbox.width} / bb.width=${bb.width} = ratio=${ratio}`
      );
      console.log(
          `OK SVGText = [${dg_svg_text.text}]`
      );
      console.log(svg_item);
      */
    } else {
      console.log(`SVG Scale factor > 20:  ${dest_bbox.width / bb.width}`);
      console.log(`width=${this.width} / orig_img_rect.width=${this.orig_img_rect.width}`);
      console.log(`dest_bbox.width=${dest_bbox.width} / bb.width=${bb.width} = ratio=${ratio}`);
      console.log(`SVGText = [${dg_svg_text.text}]`);
      console.log(svg_item);
    }

    svg_item.setAttribute("x", tx);
    svg_item.setAttribute("y", ty);
  }

  build_for(words_arr, highlight_text_arr) {
    let svg_container = this.make_svg_container();
    let that = this;
    let older_svg;

    if (this.dom_parent) {
      older_svg = this.dom_parent.querySelectorAll('svg');
      jquery__WEBPACK_IMPORTED_MODULE_0___default()(older_svg).remove();
    }

    this.dom_parent.insertBefore(svg_container, this.dom_img);
    words_arr.forEach(function (dom_item, index, array) {
      let x1 = dom_item.getAttribute('x1'),
          y1 = dom_item.getAttribute('y1'),
          x2 = dom_item.getAttribute('x2'),
          y2 = dom_item.getAttribute('y2');
      let bbox, dg_svg_text, svg_item;
      bbox = new DgBBox(x1, y1, x2, y2);
      dg_svg_text = new DgSVGText(bbox.x1, bbox.y2, dom_item.textContent);
      svg_item = dg_svg_text.make_svg();
      svg_container.appendChild(svg_item);
      that.fit_text_to_bbox(bbox, svg_item, dg_svg_text); // used to track back original words (i.e. for debugging)

      svg_item.setAttribute('id', dom_item.getAttribute('id'));
      svg_item.setAttribute('title', dom_item.getAttribute('title')); // changed to yellow when highliting text
      // as user search result.

      svg_item.setAttribute('fill', 'transparent');
      svg_item.setAttribute('opacity', '0.4');

      if (highlight_text_arr) {
        for (let word of highlight_text_arr) {
          if (word == dom_item.textContent) {
            svg_item.setAttribute('stroke', 'yellow');
            svg_item.setAttribute('stroke-width', '10');
          }
        }
      }
    });
    return svg_container;
  }

}

/***/ }),

/***/ "./src/js/utils.js":
/*!*************************!*\
  !*** ./src/js/utils.js ***!
  \*************************/
/*! exports provided: capitalize, human_size, find_by_id, get_parent_id, value, insert, proxy_click, dglReady */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "capitalize", function() { return capitalize; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "human_size", function() { return human_size; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "find_by_id", function() { return find_by_id; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "get_parent_id", function() { return get_parent_id; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "value", function() { return value; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "insert", function() { return insert; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "proxy_click", function() { return proxy_click; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "dglReady", function() { return dglReady; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);

function capitalize(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

String.prototype.format = function () {
  var i = 0,
      args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
}; // polyfill for dom.remove function for IE
// from:https://github.com/jserz/js_piece/blob/master/DOM/ChildNode/remove()/remove().md


(function (arr) {
  arr.forEach(function (item) {
    if (item.hasOwnProperty('remove')) {
      return;
    }

    Object.defineProperty(item, 'remove', {
      configurable: true,
      enumerable: true,
      writable: true,
      value: function remove() {
        if (this.parentNode === null) {
          return;
        }

        this.parentNode.removeChild(this);
      }
    });
  });
})([Element.prototype, CharacterData.prototype, DocumentType.prototype]); // Polyfill for Array.includes for IE.
// https://tc39.github.io/ecma262/#sec-array.prototype.includes


if (!Array.prototype.includes) {
  Object.defineProperty(Array.prototype, 'includes', {
    value: function (searchElement, fromIndex) {
      if (this == null) {
        throw new TypeError('"this" is null or not defined');
      } // 1. Let O be ? ToObject(this value).


      var o = Object(this); // 2. Let len be ? ToLength(? Get(O, "length")).

      var len = o.length >>> 0; // 3. If len is 0, return false.

      if (len === 0) {
        return false;
      } // 4. Let n be ? ToInteger(fromIndex).
      //    (If fromIndex is undefined, this step produces the value 0.)


      var n = fromIndex | 0; // 5. If n ≥ 0, then
      //  a. Let k be n.
      // 6. Else n < 0,
      //  a. Let k be len + n.
      //  b. If k < 0, let k be 0.

      var k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);

      function sameValueZero(x, y) {
        return x === y || typeof x === 'number' && typeof y === 'number' && isNaN(x) && isNaN(y);
      } // 7. Repeat, while k < len


      while (k < len) {
        // a. Let elementK be the result of ? Get(O, ! ToString(k)).
        // b. If SameValueZero(searchElement, elementK) is true, return true.
        if (sameValueZero(o[k], searchElement)) {
          return true;
        } // c. Increase k by 1. 


        k++;
      } // 8. Return false


      return false;
    }
  });
}

function human_size(bytes_count) {
  var arr = ['B', 'KB', 'MB', 'GB', 'TB'],
      output = "";

  if (!bytes_count) {
    console.log("Invalid bytes count provided");
    return;
  }

  ;

  for (var x = bytes_count, mult = 0; x > 1; x = x / 1024, mult++) {
    output = x.toFixed(1) + " " + arr[mult];
  }

  ;
  return output;
}
function find_by_id(dom_id) {
  if (document.getElementById(dom_id)) {
    return true;
  }

  return false;
}

function get_object_id(pathname) {
  var my_regexp = /basetreenode\/(\d+)\//g,
      match;
  match = my_regexp.exec(pathname);

  if (match != null) {
    return match[1];
  }

  return -1;
}

function get_parent_id() {
  return get_object_id(window.location.pathname);
}
function value(elem_id) {
  var elem = document.getElementById(elem_id);

  if (!elem) {
    return undefined;
  } else {
    return elem.value;
  }
}
function insert(tag_name, attrs) {
  let new_elem = document.createElement(tag_name),
      keys = Object.keys(attrs);

  for (let i = 0; i < keys.length; i++) {
    let key = keys[i],
        value = attrs[keys[i]];
    new_elem.setAttribute(key, value);
  }

  document.body.appendChild(new_elem);
}
function proxy_click(from_elem_id, to_elem_id) {
  let $from_elem = jquery__WEBPACK_IMPORTED_MODULE_0___default()(from_elem_id),
      $to_elem = jquery__WEBPACK_IMPORTED_MODULE_0___default()(to_elem_id);

  if (!$from_elem) {
    console.log("dglUtils -> proxy_click -> from_elem is not defined");
    return;
  }

  $from_elem.click(function (e) {
    e.preventDefault();

    if ($to_elem) {
      $to_elem.click();
    }
  });
}
function dglReady(func) {
  document.addEventListener('DOMContentLoaded', func);
}
;

/***/ }),

/***/ "./src/js/views/access.js":
/*!********************************!*\
  !*** ./src/js/views/access.js ***!
  \********************************/
/*! exports provided: AccessView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AccessView", function() { return AccessView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _permission_editor__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./permission_editor */ "./src/js/views/permission_editor.js");
/* harmony import */ var _models_access__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/access */ "./src/js/models/access.js");
/* harmony import */ var _models_permission__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/permission */ "./src/js/models/permission.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");








let TEMPLATE = __webpack_require__(/*! ../templates/access.html */ "./src/js/templates/access.html");

class AccessView extends backbone__WEBPACK_IMPORTED_MODULE_5__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#access-modal');
  }

  initialize(node) {
    this.acc_collection = new _models_access__WEBPACK_IMPORTED_MODULE_3__["AccessCollection"]([], {
      'node': node
    });
    this.acc_collection.fetch();
    this.node = node; // deleted items will be moved to this collection
    // and then passed to server side

    this.deleted_acc = new _models_access__WEBPACK_IMPORTED_MODULE_3__["AccessCollection"]([], {});
    this.listenTo(this.acc_collection, 'change', this.render);
    this.listenTo(_models_dispatcher__WEBPACK_IMPORTED_MODULE_6__["mg_dispatcher"], _models_dispatcher__WEBPACK_IMPORTED_MODULE_6__["PERMISSION_CHANGED"], this.on_perm_changed);
    this.render();
  }

  events() {
    let event_map = {
      'click #create_perm': 'create_perm',
      'click #edit_perm': 'edit_perm',
      'click #delete_perm': 'delete_perm',
      'click #readonly_view_perm': 'readonly_view_perm',
      'click #access_items tr': 'on_item_click',
      'click .close': 'on_close',
      'click .cancel': 'on_close',
      'click .apply': 'on_apply'
    };
    return event_map;
  }

  on_apply(event) {
    this.$el.html('');
    this.$el.modal('hide'); // removes attached events via event map

    this.undelegateEvents();
    this.acc_collection.save_access(this.deleted_acc);
  }

  on_close(event) {
    // removes attached events via event map
    this.undelegateEvents();
  }

  on_item_click(event) {
    let $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget);

    if ($target.hasClass('disabled')) {
      return;
    }

    $target.toggleClass('checked');
  }

  on_perm_changed(permission, users, groups) {
    /*****
    Permissions set and user + group to which they apply.
    ****/
    let that = this,
        perm;

    underscore__WEBPACK_IMPORTED_MODULE_1__["default"].each(users, function (item) {
      perm = new _models_permission__WEBPACK_IMPORTED_MODULE_4__["Permission"]();
      perm.set({
        'permissions': permission.get('permissions')
      });
      perm.set({
        'name': item
      });
      perm.set({
        'model': 'user'
      });
      perm.set({
        'access_type': permission.get('access_type')
      });
      perm.set({
        'access_inherited': permission.get('access_inherited')
      });
      that.acc_collection.add(perm);
    });

    underscore__WEBPACK_IMPORTED_MODULE_1__["default"].each(groups, function (item) {
      perm = new _models_permission__WEBPACK_IMPORTED_MODULE_4__["Permission"]();
      perm.set({
        'permissions': permission.get('permissions')
      });
      perm.set({
        'name': item
      });
      perm.set({
        'model': 'group'
      });
      perm.set({
        'access_type': permission.get('access_type')
      });
      perm.set({
        'access_inherited': permission.get('access_inherited')
      });
      that.acc_collection.add(perm);
    });

    that.render();
  }

  create_perm(event) {
    let perm_editor_view;
    perm_editor_view = new _permission_editor__WEBPACK_IMPORTED_MODULE_2__["PermissionEditorView"]();
  }

  edit_perm(event) {
    let perm_editor_view, found;
    found = this._first_selected();
    perm_editor_view = new _permission_editor__WEBPACK_IMPORTED_MODULE_2__["PermissionEditorView"](found);
  }

  delete_perm(event) {
    let attrs = [],
        models,
        that = this;
    attrs = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].map(this.$el.find('tr.checked'), function (item) {
      let name, model;
      name = jquery__WEBPACK_IMPORTED_MODULE_0___default()(item).data('name');
      model = jquery__WEBPACK_IMPORTED_MODULE_0___default()(item).data('model');
      return {
        'name': name,
        'model': model
      };
    });

    underscore__WEBPACK_IMPORTED_MODULE_1__["default"].each(attrs, function (attr) {
      let found = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(that.acc_collection.models, function (item) {
        return item.get('name') == attr['name'] && item.get('model') == attr['model'];
      });

      that.deleted_acc.add(found);
      that.acc_collection.remove(found);
    });

    this.render();
  }

  readonly_view_perm(event) {
    let perm_editor_view, found;
    found = this._first_selected();
    perm_editor_view = new _permission_editor__WEBPACK_IMPORTED_MODULE_2__["PermissionEditorView"](found, false // edit = false, i.e. open readonly view
    );
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      acc_collection: this.acc_collection,
      node: this.node
    }));
    this.$el.html(compiled);
    this.$el.modal();
    return this;
  }

  _first_selected() {
    /*
     * Returns first selected Permission object
    */
    let checked_el, cid, id, found;
    checked_el = this.$el.find('tr.checked');
    cid = checked_el.data('cid');
    id = checked_el.data('id');
    found = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(this.acc_collection.models, function (item) {
      return item.cid == cid || item.get('id') == id;
    });
    return found;
  }

}
;

/***/ }),

/***/ "./src/js/views/actions.js":
/*!*********************************!*\
  !*** ./src/js/views/actions.js ***!
  \*********************************/
/*! exports provided: ActionsView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ActionsView", function() { return ActionsView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _models_node__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/node */ "./src/js/models/node.js");
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");
/* harmony import */ var _views_new_folder__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../views/new_folder */ "./src/js/views/new_folder.js");
/* harmony import */ var _views_rename__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../views/rename */ "./src/js/views/rename.js");
/* harmony import */ var _views_access__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../views/access */ "./src/js/views/access.js");
/* harmony import */ var _views_uploader__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../views/uploader */ "./src/js/views/uploader.js");










class ActionsView extends backbone__WEBPACK_IMPORTED_MODULE_2__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#actions');
  }

  initialize(parent_id) {
    this.parent_id = parent_id;
    this.action_conditions = this._build_action_conditions(); // collection of nodes

    this.selection = new _models_node__WEBPACK_IMPORTED_MODULE_3__["NodeCollection"](); // collection of nodes

    this.clipboard = new backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"]();
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["PARENT_CHANGED"], this.parent_changed, this);
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["SELECTION_CHANGED"], this.selection_changed, this);
  }

  set_parent(parent_id) {
    this.parent_id = parent_id;
  }

  events() {
    let event_map = {
      'click #new-folder': 'new_folder',
      'click #delete': 'delete_node',
      'click #cut': 'cut_node',
      'click #paste': 'paste',
      'click #access': 'click_access',
      'click #paste_pages': 'paste_pages',
      'click #rename': 'rename_node',
      // will proxy event to #id_file_name
      'click #id_btn_upload': 'upload_clicked',
      'change #id_file_name': 'upload'
    };
    return event_map;
  }

  click_access(event) {
    let node = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].first(this.selection.models),
        access_view;

    if (node) {
      access_view = new _views_access__WEBPACK_IMPORTED_MODULE_7__["AccessView"](node);
    }
  }

  upload(event) {
    let $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget),
        files,
        lang = jquery__WEBPACK_IMPORTED_MODULE_0___default()("#lang").val(),
        uploader_view;
    files = $target[0].files;
    uploader_view = new _views_uploader__WEBPACK_IMPORTED_MODULE_8__["UploaderView"](files, lang, this.parent_id);
  }

  upload_clicked(event) {
    let $hidden_file_input = jquery__WEBPACK_IMPORTED_MODULE_0___default()("#id_file_name");
    event.preventDefault(); // send click event to hidden #id_file_name element
    // (input[type=file] element used for uploads)

    $hidden_file_input.click();
  }

  delete_node(event) {
    let options = {},
        confirmation,
        titles_arr,
        titles_str;

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    }; // https://stackoverflow.com/questions/10858935/cleanest-way-to-destroy-every-model-in-a-collection-in-backbone
    //_.each(_.clone(this.selection.models), function(model){
    //  model.destroy(options);
    //});


    titles_arr = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].map(this.selection.models, function (model) {
      return model.get('title');
    });
    titles_str = titles_arr.join(', ');
    confirmation = confirm(`DELETE following folders/documents:  ${titles_str}?`);

    if (!confirmation) {
      return;
    }

    this.selection.delete(options);
  }

  cut_node(event) {
    let options = {};

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    };

    this.selection.cut(options);
  }

  paste(event) {
    let options = {};

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    };

    console.log(`paste: current parent_id=${this.parent_id}`);
    this.selection.paste(options, this.parent_id);
  }

  paste_pages(event) {
    let options = {};

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    };

    this.selection.paste_pages(options, this.parent_id);
  }

  parent_changed(parent_id) {
    this.parent_id = parent_id;
    console.log(`ActionsView - parent_changed: current parent_id=${this.parent_id}`);
  }

  selection_changed(selection) {
    let that = this;
    this.selection.reset(selection);

    underscore__WEBPACK_IMPORTED_MODULE_1__["default"].each(this.action_conditions.models, function (item) {
      if (item.get('cond')(that.selection, that.clipboard, that.parent_id)) {
        that.enable_action(item);
      } else {
        that.disable_action(item);
      }
    });
  }

  rename_node(event) {
    let node = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].first(this.selection.models),
        rename_view;

    if (node) {
      rename_view = new _views_rename__WEBPACK_IMPORTED_MODULE_6__["RenameView"](node);
    }
  }

  new_folder(event) {
    let new_folder_view, parent_id;
    parent_id = this.parent_id;
    new_folder_view = new _views_new_folder__WEBPACK_IMPORTED_MODULE_5__["NewFolderView"](parent_id);
  }

  enable_action(item) {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(item.get('id')).removeClass("disabled");
  }

  disable_action(item) {
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(item.get('id')).addClass("disabled");
  }

  _build_action_conditions() {
    let that = this,
        result = new backbone__WEBPACK_IMPORTED_MODULE_2__["Collection"]();
    result.add({
      'id': "#delete",
      'cond': function (selection, clipboard, parent_id) {
        if (selection.length > 0) {
          return true;
        }

        return false;
      }
    });
    result.add({
      'id': "#cut",
      'cond': function (selection, clipboard, parent_id) {
        if (selection.length > 0) {
          return true;
        }

        return false;
      }
    });
    result.add({
      'id': "#rename",
      'cond': function (selection, clipboard, parent_id) {
        if (selection.length == 1) {
          return true;
        }

        return false;
      }
    });
    result.add({
      'id': "#access",
      'cond': function (selection, clipboard, parent_id) {
        if (selection.length == 1) {
          return true;
        }

        return false;
      }
    });
    return result;
  }

}

/***/ }),

/***/ "./src/js/views/breadcrumb.js":
/*!************************************!*\
  !*** ./src/js/views/breadcrumb.js ***!
  \************************************/
/*! exports provided: BreadcrumbView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BreadcrumbView", function() { return BreadcrumbView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_breadcrumb__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/breadcrumb */ "./src/js/models/breadcrumb.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");







let TEMPLATE = __webpack_require__(/*! ../templates/breadcrumb.html */ "./src/js/templates/breadcrumb.html");

class BreadcrumbView extends backbone__WEBPACK_IMPORTED_MODULE_3__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#breadcrumb');
  }

  initialize(parent_id) {
    let that = this;
    this.breadcrumb = new _models_breadcrumb__WEBPACK_IMPORTED_MODULE_2__["Breadcrumb"](parent_id);
    this.breadcrumb.fetch();
    this.listenTo(this.breadcrumb, 'change', this.render);
  }

  events() {
    let event_map = {
      'click .breadcrumb-node': 'open_node'
    };
    return event_map;
  }

  open_node(event) {
    let data = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).data(),
        node;
    node = this.breadcrumb.nodes.get(data['id']);

    if (node) {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["PARENT_CHANGED"], node.id);
    } else {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["PARENT_CHANGED"], undefined);
    }
  }

  open(node_id) {
    this.breadcrumb.set({
      'parent_id': node_id
    });
    this.breadcrumb.fetch();
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'nodes': this.breadcrumb.nodes
    }));
    this.$el.html(compiled);
  }

}

/***/ }),

/***/ "./src/js/views/browse.js":
/*!********************************!*\
  !*** ./src/js/views/browse.js ***!
  \********************************/
/*! exports provided: BrowseView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "BrowseView", function() { return BrowseView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_browse__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/browse */ "./src/js/models/browse.js");
/* harmony import */ var _display_mode__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./display_mode */ "./src/js/views/display_mode.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");
/* harmony import */ var _routers_browse__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../routers/browse */ "./src/js/routers/browse.js");









let TEMPLATE_GRID = __webpack_require__(/*! ../templates/browse_grid.html */ "./src/js/templates/browse_grid.html");

let TEMPLATE_LIST = __webpack_require__(/*! ../templates/browse_list.html */ "./src/js/templates/browse_list.html");

let SORT_ASC = 'asc';
let SORT_DESC = 'desc';
let SORT_UNDEFINED = 0;

class Column {
  constructor(name, key, sort) {
    this._name = name;
    this._key = key;
    this._sort = this.get_local(name) || sort;
  }

  get key() {
    return this._key;
  }

  get name() {
    return this._name;
  }

  get sort() {
    return this._sort;
  }

  set sort(sort_state) {
    this._sort = sort_state;
    this.set_local(this.name, sort_state);
  }

  get_local(name) {
    let local = localStorage.getItem(`browse_list.${name}`);

    if (local == "0" || local == undefined) {
      return SORT_UNDEFINED;
    }

    ;
    return local;
  }

  set_local(name, value) {
    localStorage.setItem(`browse_list.${name}`, value);
  }

  toggle() {
    // changes sorting state of the column
    // if sort is undefined - initial sort is ASC
    if (this.sort == SORT_UNDEFINED || this.sort == undefined) {
      this.sort = SORT_ASC;
    } else if (this.sort == SORT_ASC) {
      this.sort = SORT_DESC;
    } else if (this.sort == SORT_DESC) {
      this.sort = SORT_ASC;
    }
  }

  get sort_icon_name() {
    let fa_name = 'fa-sort';

    if (this.sort == SORT_ASC) {
      fa_name = 'fa-sort-amount-down-alt';
    } else if (this.sort == SORT_DESC) {
      fa_name = 'fa-sort-amount-down';
    }

    return fa_name;
  }

}

class Table {
  constructor(nodes, parent_kv) {
    let cols, sort_column;
    this._cols = this._build_header_cols(parent_kv);
    cols = this._cols;
    this._rows = this._build_rows(parent_kv, nodes);
    sort_column = this.get_sort_column();

    if (sort_column) {
      if (sort_column.key) {
        this.sort_key_column(sort_column.key, sort_column.sort == SORT_ASC ? -1 : 1);
      } else {
        this.sort_standard_column(sort_column.name, sort_column.sort == SORT_ASC ? -1 : 1);
      }
    }
  }

  get_sort_column() {
    let index = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].findIndex(this._cols, function (col) {
      return col.sort == SORT_ASC || col.sort == SORT_DESC;
    });

    if (index >= 0) {
      return this._cols[index];
    }

    return undefined;
  }

  get cols() {
    return this._cols;
  }

  get rows() {
    return this._rows;
  }

  get key_cols() {
    let result = [];
    result = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].filter(this.cols, function (item) {
      return item.key != undefined;
    });
    return result;
  }

  toggle_col_sort(index) {
    this._cols[index].toggle(); // Set as sort = undefined for all other columns
    // Only one column at the time is supported.


    for (let i = 0; i < this._cols.length; i++) {
      if (i != index) {
        this._cols[i].sort = SORT_UNDEFINED;
      }
    }

    return this._cols[index];
  }

  sort_key_column(key_name, sort_type) {
    function compare_keys(row1, row2) {
      let found_1, found_2;
      found_1 = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(row1, function (item) {
        return item['key'] == key_name;
      });
      found_2 = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(row2, function (item) {
        return item['key'] == key_name;
      });

      if (found_1['virtual_value'] < found_2['virtual_value']) {
        return sort_type;
      }

      if (found_1['virtual_value'] > found_2['virtual_value']) {
        return -sort_type;
      }

      return 0;
    }

    this._rows = this._rows.sort(compare_keys);
  }

  sort_standard_column(name, sort_type) {
    function compare_cols(row1, row2) {
      let found_1, found_2;
      found_1 = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(row1, function (item) {
        return item['col'] == name;
      });
      found_2 = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].find(row2, function (item) {
        return item['col'] == name;
      });

      if (found_1['virtual_value'] < found_2['virtual_value']) {
        return sort_type;
      }

      if (found_1['virtual_value'] > found_2['virtual_value']) {
        return -sort_type;
      }

      return 0;
    }

    this._rows = this._rows.sort(compare_cols);
  }

  _build_dict_for_type_col(node) {
    let value, virtual_value;

    if (node.is_document()) {
      value = `<i class="fa fa-file"></i>`;
      virtual_value = 0;
    } else {
      value = `<i class="fa fa-folder text-warning"></i>`;
      virtual_value = 1;
    }

    return {
      'id': node.get('id'),
      'cid': node.cid,
      'url': node.url,
      'col': 'type',
      'value': value,
      'virtual_value': virtual_value,
      'virtual_type': 'int'
    };
  }

  _build_dict_for_title_col(node) {
    let value, virtual_value;
    return {
      'id': node.get('id'),
      'cid': node.cid,
      'url': node.url,
      'col': 'title',
      'value': node.full_title(),
      'virtual_value': node.full_title(),
      'virtual_type': 'str'
    };
  }

  _build_dict_for_created_at_col(node) {
    let value, virtual_value;
    return {
      'id': node.get('id'),
      'cid': node.cid,
      'url': node.url,
      'col': 'created_at',
      'value': node.get('created_at'),
      'virtual_value': node.get('created_at'),
      'virtual_type': 'str'
    };
  }

  _build_rows(parent_kv, nodes) {
    let node,
        result = [],
        value,
        virtual_value,
        kvstore,
        key,
        row = [];

    for (let i = 0; i < nodes.length; i++) {
      node = nodes.at(i);
      row = [];
      row.push(this._build_dict_for_type_col(node));
      row.push(this._build_dict_for_title_col(node));

      for (let j = 0; j < parent_kv.length; j++) {
        kvstore = parent_kv.at(j);

        if (kvstore) {
          key = kvstore.get('key');
          value = node.get_page_value_for(key);
          virtual_value = node.get_page_virtual_value_for(kvstore.get('key'));
          row.push({
            'id': node.get('id'),
            'cid': node.cid,
            'url': node.url,
            'key': key,
            'value': value,
            'virtual_value': parseInt(virtual_value),
            'virtual_type': 'str'
          });
        }
      }

      row.push(this._build_dict_for_created_at_col(node));
      result.push(row);
    } // for


    return result;
  }

  _build_header_cols(parent_kv) {
    let result = [],
        kvstore,
        key,
        i; // there are always at least 3 cols: type, title and
    // created_at.
    // type is always first one
    // title is always second column
    // created_at column is always last one.

    result.push( // name, key, sort
    new Column('type', undefined, undefined));
    result.push( // name, key, sort
    new Column('title', undefined, undefined));

    for (i = 0; i < parent_kv.length; i++) {
      kvstore = parent_kv.at(i);
      key = kvstore.get('key');
      result.push(new Column(key, key, undefined));
    }

    result.push( // name, key, sort
    new Column('created_at', undefined, undefined));
    return result;
  }

}

class BrowseListView extends backbone__WEBPACK_IMPORTED_MODULE_4__["View"] {
  /**
    List mode displays a table which can be sorted by each individual column.
    Also, some columns might be added or removed.
  **/
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#browse');
  }

  initialize() {
    this._table = undefined;
  }

  get table() {
    return this._table;
  }

  get cols() {
    return this._table.cols;
  }

  get rows() {
    return this._table.rows;
  }

  events() {
    let event_map = {
      "click .header.sort": "col_sort"
    };
    return event_map;
  }

  col_sort(event) {
    let data = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).data(),
        key_name,
        column;

    if (data.col == 'key') {
      // kvstore column was clicked, find out
      // exact key name
      key_name = data.key;
      this.toggle_key_column(key_name);
    } else {
      this.toggle_standard_column(data.col);
    }

    event.preventDefault();
    this.trigger("change");
  }

  toggle_key_column(key_name) {
    let index;
    index = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].findIndex(this.cols, function (item) {
      return item.key == key_name;
    });

    if (index >= 0) {
      this.toggle_col_sort(index);
    }
  }

  toggle_col_sort(index) {
    return this._table.toggle_col_sort(index);
  }

  toggle_standard_column(name) {
    let index;
    index = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].findIndex(this.cols, function (item) {
      return item.name == name;
    });

    if (index >= 0) {
      return this.toggle_col_sort(index);
    }
  }

  render(nodes, parent_kv) {
    let compiled, context;
    context = {};
    this._table = new Table(nodes, parent_kv);
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE_LIST({
      'nodes': nodes,
      'parent_kv': parent_kv,
      'table': this.table
    }));
    this.$el.html(compiled);
  }

}

class BrowseGridView extends backbone__WEBPACK_IMPORTED_MODULE_4__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#browse');
  }

  render(nodes) {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE_GRID({
      'nodes': nodes
    }));
    this.$el.html(compiled);
  }

}

class BrowseView extends backbone__WEBPACK_IMPORTED_MODULE_4__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#browse');
  }

  initialize(parent_id) {
    this.browse = new _models_browse__WEBPACK_IMPORTED_MODULE_2__["Browse"](parent_id); // UI used to switch between list and grid display modes

    this.display_mode = new _display_mode__WEBPACK_IMPORTED_MODULE_3__["DisplayModeView"](); // there are to view modes - list and grid

    this.browse_list_view = new BrowseListView();
    this.browse_grid_view = new BrowseGridView();
    this.listenTo(this.browse, 'change', this.render);
    this.listenTo(this.display_mode, 'change', this.render);
    this.listenTo(this.browse_list_view, 'change', this.render);
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["BROWSER_REFRESH"], this.refresh, this);
  }

  events() {
    let event_map = {
      'dblclick .node': 'open_node',
      'click .node': 'select_node'
    };
    return event_map;
  }

  select_node(event) {
    let data = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).data(),
        node,
        selected,
        new_state,
        $target,
        checkbox;
    $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget);
    node = this.browse.nodes.get(data['cid']);

    if (node) {
      selected = node.get('selected');
      node.set({
        'selected': !selected
      });
      new_state = !selected;

      if (new_state) {
        $target.addClass('checked');
      } else {
        $target.removeClass('checked');
      }

      _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["SELECTION_CHANGED"], this.get_selection());
    }
  }

  get_selection() {
    let result;
    result = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].filter(this.browse.nodes.models, function (item) {
      return item.get('selected') == true;
    });
    return result;
  }

  open_node(event) {
    let data = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).data(),
        node;
    node = this.browse.nodes.get(data['cid']); // folder is 'browsed' by triggering PARENT_CHANGED event

    if (node.is_folder()) {
      // routers.browse handles PARENT_CHANGED event.
      if (node) {
        _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["PARENT_CHANGED"], node.id);
      } else {
        _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["PARENT_CHANGED"], undefined);
      }

      return;
    } // will reach this place only if node is a document.


    window.location = node.get('document_url');
  }

  open(node_id) {
    let parent_id = node_id;
    this.browse.set({
      'parent_id': node_id
    });
    this.browse.fetch();
  }

  refresh() {
    let parent_id = this.browse.get('parent_id');
    this.open(parent_id);
  }

  render() {
    let compiled, context;
    context = {};

    if (this.display_mode.is_list()) {
      this.browse_list_view.render(this.browse.nodes, this.browse.parent_kv);
    } else {
      this.browse_grid_view.render(this.browse.nodes);
    }
  }

}

/***/ }),

/***/ "./src/js/views/control_sidebar.js":
/*!*****************************************!*\
  !*** ./src/js/views/control_sidebar.js ***!
  \*****************************************/
/*! exports provided: ControlSidebarView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* WEBPACK VAR INJECTION */(function($) {/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "ControlSidebarView", function() { return ControlSidebarView; });
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./metadata */ "./src/js/views/metadata.js");
/* harmony import */ var _metadata_page__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./metadata_page */ "./src/js/views/metadata_page.js");
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");




class ControlSidebarView extends backbone__WEBPACK_IMPORTED_MODULE_0__["View"] {
  el() {
    return $('.control-sidebar');
  }

  events() {
    let events_map = {
      "click button#save": "on_save"
    };
    return events_map;
  }

  initialize() {
    this.metadata_view = undefined;
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["SELECTION_CHANGED"], this.selection_changed, this);
    _models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["mg_dispatcher"].on(_models_dispatcher__WEBPACK_IMPORTED_MODULE_3__["PAGE_SELECTION_CHANGED"], this.page_selection_changed, this);
  }

  page_selection_changed(page_id) {
    /**
    Triggered by thumbnails_list: 
        * after thumbnail list is loaded, in this case
          page_id of first thumb is passed).
        * when user clicks on any thumb.
    */
    if (!page_id) {
      return;
    }

    if (this.metadata_view) {
      this.metadata_view.stop();
      this.metadata_view = undefined;
      return;
    } // calls start() method.


    this.metadata_view = new _metadata_page__WEBPACK_IMPORTED_MODULE_2__["MetadataPageView"](page_id);
  }

  selection_changed(selection) {
    /*
        Triggered by browser view when user selects/deselects
        nodes - documents/folders
    */
    let selected_node, metadata;

    if (selection.length == 0 || selection.length != 1) {
      // nothing is selected, remove the view.
      if (this.metadata_view) {
        this.metadata_view.stop();
        this.metadata_view = undefined;
        return;
      }
    }

    selected_node = selection[0];

    if (!selected_node) {
      return;
    } // new MetadataView(...)
    // calls start() method.


    this.metadata_view = new _metadata__WEBPACK_IMPORTED_MODULE_1__["MetadataView"](selected_node.get('id'));
  }

  on_save(event) {
    this.$el.find("#save-metadata").trigger('click');
  }

}
/* WEBPACK VAR INJECTION */}.call(this, __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js")))

/***/ }),

/***/ "./src/js/views/display_mode.js":
/*!**************************************!*\
  !*** ./src/js/views/display_mode.js ***!
  \**************************************/
/*! exports provided: GRID, LIST, DisplayModeView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "GRID", function() { return GRID; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LIST", function() { return LIST; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DisplayModeView", function() { return DisplayModeView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);




let TEMPLATE = __webpack_require__(/*! ../templates/display_mode.html */ "./src/js/templates/display_mode.html");

let GRID = 'grid';
let LIST = 'list';
class DisplayModeView extends backbone__WEBPACK_IMPORTED_MODULE_2__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#display-mode');
  }

  initialize() {
    this.display = this.get_local('display_mode') || GRID;
    this.listenTo(this, "change", this.render);
    this.render();
  }

  events() {
    let events_map = {
      "click .display-list": "display_list",
      "click .display-grid": "display_grid"
    };
    return events_map;
  }

  get_local() {
    return localStorage.getItem('display_mode');
  }

  set_local(mode) {
    return localStorage.setItem('display_mode', mode);
  }

  is_list() {
    return this.display == LIST;
  }

  is_grid() {
    return this.display == GRID;
  }

  display_list(event) {
    event.preventDefault();
    this.display = LIST;
    this.set_local(LIST);
    this.trigger('change');
  }

  display_grid(event) {
    event.preventDefault();
    this.display = GRID;
    this.set_local(GRID);
    this.trigger('change');
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'is_list': this.is_list(),
      'is_grid': this.is_grid()
    }));
    this.$el.html(compiled);
  }

}

/***/ }),

/***/ "./src/js/views/document.js":
/*!**********************************!*\
  !*** ./src/js/views/document.js ***!
  \**********************************/
/*! exports provided: DocumentActionsView, add_zoom_2_document_form, DocumentView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DocumentActionsView", function() { return DocumentActionsView; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "add_zoom_2_document_form", function() { return add_zoom_2_document_form; });
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "DocumentView", function() { return DocumentView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _document_form_page_scroll__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../document_form/page_scroll */ "./src/js/document_form/page_scroll.js");
/* harmony import */ var _text_overlay__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../text_overlay */ "./src/js/text_overlay.js");
/* harmony import */ var _document_form_thumbnail_list__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../document_form/thumbnail_list */ "./src/js/document_form/thumbnail_list.js");
/* harmony import */ var _document_form_thumbnail__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../document_form/thumbnail */ "./src/js/document_form/thumbnail.js");
/* harmony import */ var _document_form_zoom__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../document_form/zoom */ "./src/js/document_form/zoom.js");
/* harmony import */ var _document_form_page_list__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../document_form/page_list */ "./src/js/document_form/page_list.js");
/* harmony import */ var _document_form_common__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../document_form/common */ "./src/js/document_form/common.js");
/* harmony import */ var _spinner__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../spinner */ "./src/js/spinner.js");
/* harmony import */ var _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ../actions/changeform_actions */ "./src/js/actions/changeform_actions.js");
/* harmony import */ var _views_breadcrumb__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../views/breadcrumb */ "./src/js/views/breadcrumb.js");
/* harmony import */ var _views_rename__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../views/rename */ "./src/js/views/rename.js");
/* harmony import */ var _models_document__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../models/document */ "./src/js/models/document.js");

















class DocumentActionsView extends backbone__WEBPACK_IMPORTED_MODULE_2__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#document-actions');
  }

  events() {
    let event_map = {
      "click #sw-left-panel": "toggle_thumbnails"
    };
    return event_map;
  }

  toggle_thumbnails(event) {
    let target_id = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).data("target-id"),
        $target;
    event.preventDefault();
    $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()("#" + target_id);

    if ($target.length == 0) {
      console.log("target " + target_id + " not found");
      return;
    }

    $target.toggle();
  }

}

function add_zoom_logic() {
  let actual_pages = Array.from(document.querySelectorAll('.actual-pages .actual_page'));
  jquery__WEBPACK_IMPORTED_MODULE_0___default()(".zoom").change(function () {
    let zoom_val = parseInt(jquery__WEBPACK_IMPORTED_MODULE_0___default()(this).val()) || 3;
    actual_pages.forEach(function (dom_page_item, index, arr) {});
  });
  jquery__WEBPACK_IMPORTED_MODULE_0___default()(".zoom").trigger("change");
} // add_zoom_logic


function add_zoom_2_document_form() {
  add_zoom_logic();
}
class DocumentView extends backbone__WEBPACK_IMPORTED_MODULE_2__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#document');
  }

  initialize() {
    let dom_actual_pages = document.querySelector('.actual_pages'),
        document_id = jquery__WEBPACK_IMPORTED_MODULE_0___default()("input[name=document_id]").val();
    this._thumbnail_list = new _document_form_thumbnail_list__WEBPACK_IMPORTED_MODULE_5__["MgThumbnailList"]();
    this._zoom = new _document_form_zoom__WEBPACK_IMPORTED_MODULE_7__["DgZoom"]();
    this._page_list = new _document_form_page_list__WEBPACK_IMPORTED_MODULE_8__["MgPageList"](this._zoom);

    this._thumbnail_list.load();

    this._page_list.load(this.zoom.get_value());

    this._spinner = new _spinner__WEBPACK_IMPORTED_MODULE_10__["DgMainSpinner"]();
    this._actions = this.build_actions();
    this._breadcrumb_view = new _views_breadcrumb__WEBPACK_IMPORTED_MODULE_12__["BreadcrumbView"](document_id);

    if (dom_actual_pages) {
      new _document_form_page_scroll__WEBPACK_IMPORTED_MODULE_3__["DgPageScroll"](dom_actual_pages);
    }

    this.configEvents();
  }

  get actions() {
    return this._actions;
  }

  get zoom() {
    return this._zoom;
  }

  get page_list() {
    return this._page_list;
  }

  scroll_to(page_num) {
    this._thumbnail_list.remove_highlights();

    this._thumbnail_list.mark_highlight(page_num);

    this._page_list.scroll_to(page_num);
  }

  on_thumbnail_dblclick(page_num) {
    this.scroll_to(page_num);
  }

  on_thumbnail_click(page_num, doc_id, page_id) {
    console.log(`Page ${page_num} ${doc_id} ${page_id} click`);
  }

  on_zoom_change(new_zoom_val) {
    this.page_list.on_zoom(new_zoom_val);
  }

  on_page_move_up(page_num, doc_id, page_id) {
    this.actions.clear_selection();

    this._thumbnail_list.clear_selections();

    this._page_list.on_page_move_up(page_num, doc_id, page_id);
  }

  on_page_move_down(page_num, doc_id, page_id) {
    this.actions.clear_selection();

    this._thumbnail_list.clear_selections();

    this._page_list.on_page_move_down(page_num, doc_id, page_id);
  }

  configEvents() {
    let that = this;

    this._thumbnail_list.ondblclick(this.on_thumbnail_dblclick, this);

    this._thumbnail_list.onclick(this.on_thumbnail_click, this);

    this._thumbnail_list.subscribe(_document_form_thumbnail__WEBPACK_IMPORTED_MODULE_6__["MgThumbnail"].MOVE_UP, that.on_page_move_up, that);

    this._thumbnail_list.subscribe(_document_form_thumbnail__WEBPACK_IMPORTED_MODULE_6__["MgThumbnail"].MOVE_DOWN, that.on_page_move_down, that);

    this.zoom.subscribe("zoom", this.on_zoom_change, this);
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(window).resize(function () {
      let zoom_val = that.zoom.get_value();
      console.log("window resized");
      that.page_list.on_zoom(zoom_val);
    });
  }

  build_actions() {
    /**
    Actions dropdown menu of changeform view.
    */
    let actions = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormActions"](this._thumbnail_list, this._page_list),
        rename_action,
        delete_page_action,
        cut_page_action,
        paste_page_action,
        paste_page_before_action,
        paste_page_after_action,
        apply_reorder_changes,
        that = this;
    rename_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      // Achtung! #rename id is same for rename action
      // in changeform view and changelist view.
      id: "#rename",
      enabled: function (selection, clipboard) {
        return true;
      },
      action: function (selection, clipboard, current_node) {
        let rename_view,
            node,
            options = {};
        node = new _models_document__WEBPACK_IMPORTED_MODULE_14__["Document"](current_node.id);

        function update_breadcrumb() {
          that._breadcrumb_view.breadcrumb.fetch();
        }

        options['success'] = function (model, response, options) {
          rename_view = new _views_rename__WEBPACK_IMPORTED_MODULE_13__["RenameView"](model);
          rename_view.rename.on("change", update_breadcrumb);
        };

        node.fetch(options);
      }
    });
    delete_page_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#delete-page",
      enabled: function (selection, clipboard) {
        let order_changed = false; // User cannot delete pages if he changed their
        // order and changes are pending. He/She must 
        // apply reorder changes!

        for (let page of selection.all()) {
          if (page.page_num != page.page_order) {
            return false;
          }
        }

        return selection.length > 0;
      },
      action: function (selection, clipboard, current_node, thumbnail_list, page_list) {
        let delete_page_form,
            confirmation = confirm("Are you sure?"),
            url,
            params,
            pages = [],
            doc_id;

        if (!confirmation) {
          return;
        }

        for (let page of selection.all()) {
          doc_id = page.doc_id;
          pages.push(page.page_num);
        }

        url = `/api/document/${doc_id}/pages?`;
        params = jquery__WEBPACK_IMPORTED_MODULE_0___default.a.param({
          'pages': pages
        });
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.ajax({
          url: url + params,
          method: 'DELETE'
        });
        thumbnail_list.delete_selected(selection);
        page_list.delete_selected(selection);
      }
    });
    cut_page_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#cut-page",
      enabled: function (selection, clipboard) {
        return selection.length > 0;
      },
      action: function (selection, clipboard, current_node) {
        let url,
            pages = [],
            doc_id;

        for (let page of selection.all()) {
          doc_id = page.doc_id;
          pages.push(page.page_num);
        }

        url = `/api/document/${doc_id}/pages/cut`;
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.post({
          url: url,
          type: 'POST',
          data: JSON.stringify(pages),
          dataType: "json",
          contentType: "application/json; charset=utf-8"
        });
      }
    });
    paste_page_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#paste-page",
      enabled: function (selection, clipboard) {
        return true;
      },
      action: function (selection, clipboard, current_node) {
        let url;
        url = `/api/document/${current_node.id}/pages/paste`;
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.post({
          url: url,
          type: 'POST',
          dataType: "json",
          contentType: "application/json; charset=utf-8"
        });
      }
    });
    paste_page_before_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#paste-page-before",
      enabled: function (selection, clipboard) {
        return selection.length == 1;
      },
      action: function (selection, clipboard, current_node) {
        let url,
            page_num = -1;

        for (let page of selection.all()) {
          if (page.page_num) {
            page_num = page.page_num;
          }
        }

        url = `/api/document/${current_node.id}/pages/paste`;
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.post({
          url: url,
          type: 'POST',
          data: JSON.stringify({
            'before': page_num
          }),
          dataType: "json",
          contentType: "application/json; charset=utf-8"
        });
      }
    });
    paste_page_after_action = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#paste-page-after",
      enabled: function (selection, clipboard) {
        return selection.length == 1;
      },
      action: function (selection, clipboard, current_node) {
        let url,
            page_num = -1;

        for (let page of selection.all()) {
          if (page.page_num) {
            page_num = page.page_num;
          }
        }

        url = `/api/document/${current_node.id}/pages/paste`;
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.post({
          url: url,
          type: 'POST',
          data: JSON.stringify({
            'after': page_num
          }),
          dataType: "json",
          contentType: "application/json; charset=utf-8"
        });
      }
    });
    apply_reorder_changes = new _actions_changeform_actions__WEBPACK_IMPORTED_MODULE_11__["MgChangeFormAction"]({
      id: "#apply-reorder-changes",
      enabled: function (selection, clipboard, current_node, thumbnail_list, page_list) {
        // if any page has page_num != page_order
        // it means page was reordered => there pending
        // changes.
        if (!thumbnail_list) {
          return false;
        }

        for (let thumb of thumbnail_list.all()) {
          let data = _document_form_thumbnail__WEBPACK_IMPORTED_MODULE_6__["MgThumbnail"].get_data_from_dom(thumb.dom_ref);

          if (data['page_num'] != data['page_order']) {
            return true;
          }
        }

        return false;
      },
      action: function (selection, clipboard, current_node, thumbnail_list, page_list) {
        let confirmation = confirm("Are you sure?"),
            url,
            params,
            pages = [],
            doc_id,
            data;

        if (!confirmation) {
          return;
        }

        for (let thumb of thumbnail_list.all()) {
          data = _document_form_thumbnail__WEBPACK_IMPORTED_MODULE_6__["MgThumbnail"].get_data_from_dom(thumb.dom_ref);
          doc_id = thumb.doc_id;
          pages.push({
            'page_num': data['page_num'],
            'page_order': data['page_order']
          });
        }

        url = `/api/document/${doc_id}/pages`;
        jquery__WEBPACK_IMPORTED_MODULE_0___default.a.post({
          url: url,
          type: 'POST',
          data: JSON.stringify(pages),
          dataType: "json",
          contentType: "application/json; charset=utf-8"
        });
      }
    });
    actions.add(rename_action);
    actions.add(delete_page_action);
    actions.add(cut_page_action);
    actions.add(paste_page_action);
    actions.add(paste_page_before_action);
    actions.add(paste_page_after_action);
    actions.add(apply_reorder_changes);
    return actions;
  }

}

/***/ }),

/***/ "./src/js/views/metadata.js":
/*!**********************************!*\
  !*** ./src/js/views/metadata.js ***!
  \**********************************/
/*! exports provided: MetadataView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MetadataView", function() { return MetadataView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_metadata__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/metadata */ "./src/js/models/metadata.js");
/* harmony import */ var _models_kvstore__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/kvstore */ "./src/js/models/kvstore.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_4__);






let TEMPLATE = __webpack_require__(/*! ../templates/metadata.html */ "./src/js/templates/metadata.html");

class MetadataView extends backbone__WEBPACK_IMPORTED_MODULE_4__["View"] {
  /***
      Manages the sidebar control (the one on the left side)
      view for metadata (of files and folder).
      Sidebar control contains other views besides this one.
  **/
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#metadata');
  }

  initialize(doc_id) {
    this.metadata = new _models_metadata__WEBPACK_IMPORTED_MODULE_2__["Metadata"](doc_id);
    this.start();
    this.render();
  }

  get all_disabled() {
    return this.metadata.all_disabled;
  }

  start() {
    // start listening on this.metadata object
    // which will trigger view rendering
    this.listenTo(this.metadata, 'change', this.render);
  }

  stop() {
    // stops listening
    // and remove html associated to this elem.
    this.stopListening(this.metadata);
    this.$el.html('');
  }

  events() {
    let event_map = {
      "click #add_simple_meta": "add_simple_meta",
      "click .close.key": "remove_meta",
      "keyup input": "update_value",
      "change input": "update_value",
      "change .kv_type": "kv_type_update",
      "change .kv_format": "kv_format_update",
      "click button.save": "on_save"
    };
    return event_map;
  }

  kv_format_update(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    this.metadata.update_simple(data['cid'], 'kv_format', value);
    this.render();
  }

  kv_type_update(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    let cur_fmt = {};
    cur_fmt['money'] = this.metadata.get('currency_formats');
    cur_fmt['numeric'] = this.metadata.get('numeric_formats');
    cur_fmt['date'] = this.metadata.get('date_formats');
    cur_fmt['text'] = [];
    this.metadata.update_simple(data['cid'], 'kv_type', value);
    this.metadata.update_simple(data['cid'], 'current_formats', cur_fmt[value]);

    if (cur_fmt[value].length > 0) {
      // kv_format entry is a 2 items array. First one is used as value
      // in HTML <option> and second one is the human text
      // cur_fmt[value][0][0] == use first *value* of first format from the list
      this.metadata.update_simple(data['cid'], 'kv_format', cur_fmt[value][0][0]);
    } else {
      // current list of formatting types is empty only for kv_type text
      // no formating - means kv_type = text
      this.metadata.update_simple(data['cid'], 'kv_format', "");
    }

    this.render();
  }

  update_value(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    this.metadata.update_simple(data['cid'], 'key', value);
  }

  add_simple_meta(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    this.metadata.add_simple();
    this.render();
  }

  remove_meta(event) {
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).parent();
    let $li_container = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    this.metadata.remove_simple(data['cid']);
    $li_container.remove();
    this.render();
  }

  on_save() {
    this.metadata.save();
  }

  render() {
    let compiled, context;
    context = {
      'kvstore': this.metadata.get('kvstore'),
      'available_types': this.metadata.get('kv_types')
    };
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      kvstore: this.metadata.kvstore,
      available_types: this.metadata.get('kv_types'),
      all_disabled: this.all_disabled
    }));
    this.$el.html(compiled);
    return this;
  }

}
;

/***/ }),

/***/ "./src/js/views/metadata_page.js":
/*!***************************************!*\
  !*** ./src/js/views/metadata_page.js ***!
  \***************************************/
/*! exports provided: MetadataPageView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MetadataPageView", function() { return MetadataPageView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_metadata_page__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/metadata_page */ "./src/js/models/metadata_page.js");
/* harmony import */ var _metadata__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./metadata */ "./src/js/views/metadata.js");
/* harmony import */ var _models_kvstore__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/kvstore */ "./src/js/models/kvstore.js");






let TEMPLATE = __webpack_require__(/*! ../templates/metadata_page.html */ "./src/js/templates/metadata_page.html");

class MetadataPageView extends _metadata__WEBPACK_IMPORTED_MODULE_3__["MetadataView"] {
  /***
      Manages the sidebar control (the one on the left side)
      view for metadata (of specific page within document).
      Sidebar control contains other views besides this one.
  **/
  initialize(page_id) {
    // metadata per page
    this.metadata = new _models_metadata_page__WEBPACK_IMPORTED_MODULE_2__["MetadataPage"](page_id);
    this.start();
    this.render();
  }

  events() {
    let event_map = {
      "click #add_simple_meta": "add_simple_meta",
      "click .close.key": "remove_meta",
      "keyup input[name='key']": "update_key",
      // event triggered when user - instead of typing
      // chooses a value from dropdown - native agent autocomplete feature
      "change input[name='key']": "update_key",
      "keyup input[name='value']": "update_value",
      // event triggered when user - instead of typing
      // chooses a value from dropdown - native agent autocomplete feature
      "change input[name='value']": "update_value",
      "change .kv_type": "kv_type_update",
      "change .kv_format": "kv_format_update",
      "click button.save": "on_save",
      "click .chevron.toggle": "toggle_details"
    };
    return event_map;
  }

  toggle_details(event) {
    let $current = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget);
    let parent = $current.closest("li"),
        icon_tags;
    parent.find(".details").toggleClass("d-none");
    icon_tags = $current.find("i.fa");
    icon_tags.toggleClass("fa-chevron-left");
    icon_tags.toggleClass("fa-chevron-down");
  }

  update_value(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    this.metadata.update_simple(data['cid'], 'value', value);
  }

  update_key(event) {
    let value = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).val();
    let parent = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget).closest("li");
    let data = parent.data();
    this.metadata.update_simple(data['cid'], 'key', value);
  }

  render() {
    let compiled, context;
    context = {
      'kvstore': this.metadata.get('kvstore'),
      'available_types': this.metadata.get('kv_types')
    };
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      kvstore: this.metadata.kvstore,
      available_types: this.metadata.get('kv_types'),
      all_disabled: this.all_disabled
    }));
    this.$el.html(compiled);
    return this;
  }

}

/***/ }),

/***/ "./src/js/views/new_folder.js":
/*!************************************!*\
  !*** ./src/js/views/new_folder.js ***!
  \************************************/
/*! exports provided: NewFolderView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "NewFolderView", function() { return NewFolderView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_new_folder__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/new_folder */ "./src/js/models/new_folder.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");







let TEMPLATE = __webpack_require__(/*! ../templates/new_folder.html */ "./src/js/templates/new_folder.html");

class NewFolderView extends backbone__WEBPACK_IMPORTED_MODULE_3__["View"] {
  el() {
    // this element is defined in admin/_forms.js.html
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#new-folder-modal');
  }

  initialize(parent_id) {
    this.folder = new _models_new_folder__WEBPACK_IMPORTED_MODULE_2__["NewFolder"](parent_id);
    this.render();
  }

  events() {
    let event_map = {
      "click .create": "on_create",
      "submit": "on_form_submit"
    };
    return event_map;
  }

  on_form_submit(event) {
    event.preventDefault();
    this.on_create(event);
  }

  on_create(event) {
    let folder_title,
        parent_id,
        options = {};

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    };

    folder_title = this.$el.find("[name=title]").val();

    if (folder_title == null || folder_title.trim().length === 0) {
      this.$el.modal('hide');
      return;
    }

    this.folder.set({
      'title': folder_title
    });
    this.$el.modal('hide');
    this.folder.save({}, options);
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'name': this.folder.get('name')
    }));
    this.$el.html(compiled);
    this.$el.modal();
  }

}

/***/ }),

/***/ "./src/js/views/permission_editor.js":
/*!*******************************************!*\
  !*** ./src/js/views/permission_editor.js ***!
  \*******************************************/
/*! exports provided: PermissionEditorView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "PermissionEditorView", function() { return PermissionEditorView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_permission__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/permission */ "./src/js/models/permission.js");
/* harmony import */ var _models_user_group__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../models/user_group */ "./src/js/models/user_group.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");







let TEMPLATE = __webpack_require__(/*! ../templates/permission_editor.html */ "./src/js/templates/permission_editor.html");

class PermissionEditorView extends backbone__WEBPACK_IMPORTED_MODULE_4__["View"] {
  el() {
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#permission-editor-modal');
  }

  initialize(permission, edit = true) {
    if (permission) {
      this._permission = permission;
    } else {
      this._permission = new _models_permission__WEBPACK_IMPORTED_MODULE_2__["Permission"]();
    }

    this._edit = edit;
    this._users = [];
    this._groups = [];
    this._usergroups = new _models_user_group__WEBPACK_IMPORTED_MODULE_3__["UserGroupCollection"]();

    this._usergroups.fetch();

    this.listenTo(this._usergroups, 'change', this.render);
  }

  events() {
    let event_map = {
      'click .apply': 'on_apply',
      'change .perm_user_or_group': 'on_perm_user_or_group',
      'change .access_type': 'on_access_type',
      'click .checkbox': 'on_checkbox'
    };
    return event_map;
  }

  on_perm_user_or_group(event) {
    let user_or_groups,
        name,
        model,
        that = this;
    this._users = [];
    this._groups = [];
    jquery__WEBPACK_IMPORTED_MODULE_0___default()(".perm_user_or_group :selected").each(function (i, sel) {
      name = jquery__WEBPACK_IMPORTED_MODULE_0___default()(sel).val();
      model = jquery__WEBPACK_IMPORTED_MODULE_0___default()(sel).data('model');

      if (model == 'user') {
        that._users.push(name);
      } else if (model == 'group') {
        that._groups.push(name);
      }
    });
    console.log(this._groups);
  }

  on_access_type(event) {
    let $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget),
        access_type;
    access_type = $target.val();
    this.set_type(access_type);
  }

  on_checkbox(event) {
    let $target = jquery__WEBPACK_IMPORTED_MODULE_0___default()(event.currentTarget),
        name,
        checked;
    name = $target.attr('name');
    checked = $target.is(':checked');
    this.set_perm(name, checked);
  }

  set_perm(name, checked) {
    this._permission.set_perm(name, checked);
  }

  set_type(access_type) {
    this._permission.set_type(access_type);
  }

  on_apply(event) {
    if (this._edit) {
      /* 
         means form was opened in edit mode,
         maybe something changed.
       */
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_5__["PERMISSION_CHANGED"], this._permission, this._users, this._groups);
    }

    this.$el.html('');
    this.$el.modal('hide'); // removes attached events via event map

    this.undelegateEvents();
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'usergroups': this._usergroups,
      'permission': this._permission,
      'edit': this._edit
    }));
    this.$el.html(compiled);
    this.$el.modal();
    return this;
  }

}
;

/***/ }),

/***/ "./src/js/views/rename.js":
/*!********************************!*\
  !*** ./src/js/views/rename.js ***!
  \********************************/
/*! exports provided: RenameView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "RenameView", function() { return RenameView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_rename__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/rename */ "./src/js/models/rename.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");







let TEMPLATE = __webpack_require__(/*! ../templates/rename.html */ "./src/js/templates/rename.html");

class RenameView extends backbone__WEBPACK_IMPORTED_MODULE_3__["View"] {
  el() {
    // this element is defined in admin/_forms.js.html
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#rename-modal');
  }

  initialize(node) {
    this.rename = new _models_rename__WEBPACK_IMPORTED_MODULE_2__["Rename"](node);
    this.node = node;
    this.render();
  }

  events() {
    let event_map = {
      "click .rename": "on_rename",
      "submit": "on_form_submit"
    };
    return event_map;
  }

  on_form_submit(event) {
    event.preventDefault();
    this.on_rename(event);
  }

  on_rename(event) {
    let node_title,
        parent_id,
        options = {};

    options['success'] = function () {
      _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["mg_dispatcher"].trigger(_models_dispatcher__WEBPACK_IMPORTED_MODULE_4__["BROWSER_REFRESH"]);
    };

    node_title = this.$el.find("[name=title]").val();

    if (node_title == null || node_title.trim().length === 0) {
      this.$el.modal('hide');
      return;
    }

    this.rename.set({
      'title': node_title
    });
    this.$el.modal('hide');
    this.rename.save({}, options);
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'title': this.node.get('title')
    }));
    this.$el.html(compiled);
    this.$el.modal();
  }

}

/***/ }),

/***/ "./src/js/views/uploader.js":
/*!**********************************!*\
  !*** ./src/js/views/uploader.js ***!
  \**********************************/
/*! exports provided: UploaderView */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "UploaderView", function() { return UploaderView; });
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var underscore__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! underscore */ "./node_modules/underscore/modules/index-all.js");
/* harmony import */ var _models_uploader__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../models/uploader */ "./src/js/models/uploader.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! backbone */ "./node_modules/backbone/backbone.js");
/* harmony import */ var backbone__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(backbone__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _models_dispatcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../models/dispatcher */ "./src/js/models/dispatcher.js");







let TEMPLATE = __webpack_require__(/*! ../templates/uploader.html */ "./src/js/templates/uploader.html");

class UploaderView extends backbone__WEBPACK_IMPORTED_MODULE_3__["View"] {
  el() {
    // this element is defined in admin/_forms.js.html
    return jquery__WEBPACK_IMPORTED_MODULE_0___default()('#uploader-view');
  }

  initialize(files, lang, parent_id) {
    this.uploader = new _models_uploader__WEBPACK_IMPORTED_MODULE_2__["Uploader"]();

    for (let file of files) {
      this.uploader.add(new _models_uploader__WEBPACK_IMPORTED_MODULE_2__["UploaderItem"](file, lang, parent_id));
    }

    this.listenTo(this.uploader, 'change', this.render);
    this.render();
  }

  events() {
    let event_map = {
      'click .close': 'close',
      'click button.toggle-details': 'toggle_details'
    };
    return event_map;
  }

  toggle_details(event) {
    this.$el.find('.uploader-details').toggleClass('hidden');
  }

  close(event) {
    this.$el.html('');
  }

  render() {
    let compiled, context;
    context = {};
    compiled = underscore__WEBPACK_IMPORTED_MODULE_1__["default"].template(TEMPLATE({
      'files': this.uploader
    }));
    this.$el.html(compiled);
  }

}

/***/ }),

/***/ "./src/sass/app.scss":
/*!***************************!*\
  !*** ./src/sass/app.scss ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ 0:
/*!*************************************************!*\
  !*** multi ./src/js/app.js ./src/sass/app.scss ***!
  \*************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

__webpack_require__(/*! ./src/js/app.js */"./src/js/app.js");
module.exports = __webpack_require__(/*! ./src/sass/app.scss */"./src/sass/app.scss");


/***/ })

/******/ });
//# sourceMappingURL=papermerge.js.map