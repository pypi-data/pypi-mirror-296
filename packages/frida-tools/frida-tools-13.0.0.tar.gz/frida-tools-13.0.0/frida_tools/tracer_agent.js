(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
(function (global){(function (){
"use strict";

class e {
  constructor() {
    this.handlers = new Map, this.stagedPlanRequest = null, this.stackDepth = new Map, 
    this.traceState = {}, this.nextId = 1, this.started = Date.now(), this.pendingEvents = [], 
    this.flushTimer = null, this.cachedModuleResolver = null, this.cachedObjcResolver = null, 
    this.cachedSwiftResolver = null, this.flush = () => {
      if (null !== this.flushTimer && (clearTimeout(this.flushTimer), this.flushTimer = null), 
      0 === this.pendingEvents.length) return;
      const e = this.pendingEvents;
      this.pendingEvents = [], send({
        type: "events:add",
        events: e
      });
    };
  }
  init(e, t, s, n) {
    const a = global;
    a.stage = e, a.parameters = t, a.state = this.traceState, a.defineHandler = e => e;
    for (const e of s) try {
      (0, eval)(e.source);
    } catch (t) {
      throw new Error(`Unable to load ${e.filename}: ${t.stack}`);
    }
    this.start(n).catch((e => {
      send({
        type: "agent:error",
        message: e.message
      });
    }));
  }
  dispose() {
    this.flush();
  }
  update(e, t, s) {
    const n = this.handlers.get(e);
    if (void 0 === n) throw new Error("Invalid target ID");
    const a = this.parseHandler(t, s);
    n[0] = a[0], n[1] = a[1];
  }
  async stageTargets(e) {
    const t = await this.createPlan(e);
    this.stagedPlanRequest = t, await t.ready;
    const {plan: s} = t, n = [];
    let a = 1;
    for (const [e, t, o] of s.native.values()) n.push([ a, t, o ]), a++;
    a = -1;
    for (const e of s.java) for (const [t, s] of e.classes.entries()) for (const e of s.methods.values()) n.push([ a, t, e ]), 
    a--;
    return n;
  }
  async commitTargets(e) {
    const t = this.stagedPlanRequest;
    this.stagedPlanRequest = null;
    let {plan: s} = t;
    null !== e && (s = this.cropStagedPlan(s, e));
    const n = await this.traceNativeTargets(s.native);
    let a = [];
    return 0 !== s.java.length && (a = await new Promise(((e, t) => {
      Java.perform((() => {
        this.traceJavaTargets(s.java).then(e, t);
      }));
    }))), [ ...n, ...a ];
  }
  cropStagedPlan(e, t) {
    let s;
    if (t < 0) {
      s = -1;
      for (const n of e.java) for (const [e, a] of n.classes.entries()) for (const [o, r] of a.methods.entries()) {
        if (s === t) {
          const t = {
            methods: new Map([ [ o, r ] ])
          }, s = {
            loader: n.loader,
            classes: new Map([ [ e, t ] ])
          };
          return {
            native: new Map,
            java: [ s ]
          };
        }
        s--;
      }
    } else {
      s = 1;
      for (const [n, a] of e.native.entries()) {
        if (s === t) return {
          native: new Map([ [ n, a ] ]),
          java: []
        };
        s++;
      }
    }
    throw new Error("invalid staged item ID");
  }
  async start(e) {
    const t = await this.createPlan(e, (async e => {
      await this.traceJavaTargets(e.java);
    }));
    await this.traceNativeTargets(t.plan.native), send({
      type: "agent:initialized"
    }), t.ready.then((() => {
      send({
        type: "agent:started",
        count: this.handlers.size
      });
    }));
  }
  async createPlan(e, t = async () => {}) {
    const s = {
      native: new Map,
      java: []
    }, n = [];
    for (const [t, a, o] of e) switch (a) {
     case "module":
      "include" === t ? this.includeModule(o, s) : this.excludeModule(o, s);
      break;

     case "function":
      "include" === t ? this.includeFunction(o, s) : this.excludeFunction(o, s);
      break;

     case "relative-function":
      "include" === t && this.includeRelativeFunction(o, s);
      break;

     case "imports":
      "include" === t && this.includeImports(o, s);
      break;

     case "objc-method":
      "include" === t ? this.includeObjCMethod(o, s) : this.excludeObjCMethod(o, s);
      break;

     case "swift-func":
      "include" === t ? this.includeSwiftFunc(o, s) : this.excludeSwiftFunc(o, s);
      break;

     case "java-method":
      n.push([ t, o ]);
      break;

     case "debug-symbol":
      "include" === t && this.includeDebugSymbol(o, s);
    }
    let a, o = !0;
    if (n.length > 0) {
      if (!Java.available) throw new Error("Java runtime is not available");
      a = new Promise(((e, a) => {
        Java.perform((async () => {
          o = !1;
          try {
            for (const [e, t] of n) "include" === e ? this.includeJavaMethod(t, s) : this.excludeJavaMethod(t, s);
            await t(s), e();
          } catch (e) {
            a(e);
          }
        }));
      }));
    } else a = Promise.resolve();
    return o || await a, {
      plan: s,
      ready: a
    };
  }
  async traceNativeTargets(e) {
    const t = new Map, s = new Map, n = new Map;
    for (const [a, [o, r, i]] of e.entries()) {
      let e;
      switch (o) {
       case "c":
        e = t;
        break;

       case "objc":
        e = s;
        break;

       case "swift":
        e = n;
      }
      let c = e.get(r);
      void 0 === c && (c = [], e.set(r, c)), c.push([ i, ptr(a) ]);
    }
    const [a, o, r] = await Promise.all([ this.traceNativeEntries("c", t), this.traceNativeEntries("objc", s), this.traceNativeEntries("swift", n) ]);
    return [ ...a, ...o, ...r ];
  }
  async traceNativeEntries(e, s) {
    if (0 === s.size) return [];
    const n = this.nextId, a = [], o = {
      type: "handlers:get",
      flavor: e,
      baseId: n,
      scopes: a
    };
    for (const [e, t] of s.entries()) a.push({
      name: e,
      members: t.map((e => e[0]))
    }), this.nextId += t.length;
    const {scripts: r} = await t(o), i = [];
    let c = 0;
    for (const e of s.values()) for (const [t, s] of e) {
      const e = n + c, a = "string" == typeof t ? t : t[1], o = this.parseHandler(a, r[c]);
      this.handlers.set(e, o);
      try {
        Interceptor.attach(s, this.makeNativeListenerCallbacks(e, o));
      } catch (e) {
        send({
          type: "agent:warning",
          message: `Skipping "${t}": ${e.message}`
        });
      }
      i.push(e), c++;
    }
    return i;
  }
  async traceJavaTargets(e) {
    const s = this.nextId, n = [], a = {
      type: "handlers:get",
      flavor: "java",
      baseId: s,
      scopes: n
    };
    for (const t of e) for (const [e, {methods: s}] of t.classes.entries()) {
      const t = e.split("."), a = t[t.length - 1], o = Array.from(s.keys()).map((e => [ e, `${a}.${e}` ]));
      n.push({
        name: e,
        members: o
      }), this.nextId += o.length;
    }
    const {scripts: o} = await t(a);
    return new Promise((t => {
      Java.perform((() => {
        const n = [];
        let a = 0;
        for (const t of e) {
          const e = Java.ClassFactory.get(t.loader);
          for (const [r, {methods: i}] of t.classes.entries()) {
            const t = e.use(r);
            for (const [e, r] of i.entries()) {
              const i = s + a, c = this.parseHandler(r, o[a]);
              this.handlers.set(i, c);
              const l = t[e];
              for (const e of l.overloads) e.implementation = this.makeJavaMethodWrapper(i, e, c);
              n.push(i), a++;
            }
          }
        }
        t(n);
      }));
    }));
  }
  makeNativeListenerCallbacks(e, t) {
    const s = this;
    return {
      onEnter(n) {
        s.invokeNativeHandler(e, t[0], this, n, ">");
      },
      onLeave(n) {
        s.invokeNativeHandler(e, t[1], this, n, "<");
      }
    };
  }
  makeJavaMethodWrapper(e, t, s) {
    const n = this;
    return function(...a) {
      return n.handleJavaInvocation(e, t, s, this, a);
    };
  }
  handleJavaInvocation(e, t, s, n, a) {
    this.invokeJavaHandler(e, s[0], n, a, ">");
    const o = t.apply(n, a), r = this.invokeJavaHandler(e, s[1], n, o, "<");
    return void 0 !== r ? r : o;
  }
  invokeNativeHandler(e, t, s, n, a) {
    const o = Date.now() - this.started, r = s.threadId, i = this.updateDepth(r, a);
    t.call(s, ((...t) => {
      this.emit([ e, o, r, i, t.join(" ") ]);
    }), n, this.traceState);
  }
  invokeJavaHandler(e, t, s, n, a) {
    const o = Date.now() - this.started, r = Process.getCurrentThreadId(), i = this.updateDepth(r, a), c = (...t) => {
      this.emit([ e, o, r, i, t.join(" ") ]);
    };
    try {
      return t.call(s, c, n, this.traceState);
    } catch (e) {
      if (void 0 !== e.$h) throw e;
      Script.nextTick((() => {
        throw e;
      }));
    }
  }
  updateDepth(e, t) {
    const s = this.stackDepth;
    let n = s.get(e) ?? 0;
    return ">" === t ? s.set(e, n + 1) : (n--, 0 !== n ? s.set(e, n) : s.delete(e)), 
    n;
  }
  parseHandler(e, t) {
    const s = `/handlers/${e}.js`;
    try {
      const e = Script.evaluate(s, t);
      return [ e.onEnter ?? f, e.onLeave ?? f ];
    } catch (e) {
      return send({
        type: "agent:warning",
        message: `${s}: ${e.message}`
      }), [ f, f ];
    }
  }
  includeModule(e, t) {
    const {native: s} = t;
    for (const t of this.getModuleResolver().enumerateMatches(`exports:${e}!*`)) s.set(t.address.toString(), n(t));
  }
  excludeModule(e, t) {
    const {native: s} = t;
    for (const t of this.getModuleResolver().enumerateMatches(`exports:${e}!*`)) s.delete(t.address.toString());
  }
  includeFunction(e, t) {
    const s = i(e), {native: a} = t;
    for (const e of this.getModuleResolver().enumerateMatches(`exports:${s.module}!${s.function}`)) a.set(e.address.toString(), n(e));
  }
  excludeFunction(e, t) {
    const s = i(e), {native: n} = t;
    for (const e of this.getModuleResolver().enumerateMatches(`exports:${s.module}!${s.function}`)) n.delete(e.address.toString());
  }
  includeRelativeFunction(e, t) {
    const s = c(e), n = Module.getBaseAddress(s.module).add(s.offset);
    t.native.set(n.toString(), [ "c", s.module, `sub_${s.offset.toString(16)}` ]);
  }
  includeImports(e, t) {
    let s;
    if (null === e) {
      const e = Process.enumerateModules()[0].path;
      s = this.getModuleResolver().enumerateMatches(`imports:${e}!*`);
    } else s = this.getModuleResolver().enumerateMatches(`imports:${e}!*`);
    const {native: a} = t;
    for (const e of s) a.set(e.address.toString(), n(e));
  }
  includeObjCMethod(e, t) {
    const {native: s} = t;
    for (const t of this.getObjcResolver().enumerateMatches(e)) s.set(t.address.toString(), a(t));
  }
  excludeObjCMethod(e, t) {
    const {native: s} = t;
    for (const t of this.getObjcResolver().enumerateMatches(e)) s.delete(t.address.toString());
  }
  includeSwiftFunc(e, t) {
    const {native: s} = t;
    for (const t of this.getSwiftResolver().enumerateMatches(`functions:${e}`)) s.set(t.address.toString(), o(t));
  }
  excludeSwiftFunc(e, t) {
    const {native: s} = t;
    for (const t of this.getSwiftResolver().enumerateMatches(`functions:${e}`)) s.delete(t.address.toString());
  }
  includeJavaMethod(e, t) {
    const s = t.java, n = Java.enumerateMethods(e);
    for (const e of n) {
      const {loader: t} = e, n = h(s, (e => {
        const {loader: s} = e;
        return null !== s && null !== t ? s.equals(t) : s === t;
      }));
      if (void 0 === n) {
        s.push(l(e));
        continue;
      }
      const {classes: a} = n;
      for (const t of e.classes) {
        const {name: e} = t, s = a.get(e);
        if (void 0 === s) {
          a.set(e, d(t));
          continue;
        }
        const {methods: n} = s;
        for (const e of t.methods) {
          const t = u(e), s = n.get(t);
          void 0 === s ? n.set(t, e) : n.set(t, e.length > s.length ? e : s);
        }
      }
    }
  }
  excludeJavaMethod(e, t) {
    const s = t.java, n = Java.enumerateMethods(e);
    for (const e of n) {
      const {loader: t} = e, n = h(s, (e => {
        const {loader: s} = e;
        return null !== s && null !== t ? s.equals(t) : s === t;
      }));
      if (void 0 === n) continue;
      const {classes: a} = n;
      for (const t of e.classes) {
        const {name: e} = t, s = a.get(e);
        if (void 0 === s) continue;
        const {methods: n} = s;
        for (const e of t.methods) {
          const t = u(e);
          n.delete(t);
        }
      }
    }
  }
  includeDebugSymbol(e, t) {
    const {native: s} = t;
    for (const t of DebugSymbol.findFunctionsMatching(e)) s.set(t.toString(), r(t));
  }
  emit(e) {
    this.pendingEvents.push(e), null === this.flushTimer && (this.flushTimer = setTimeout(this.flush, 50));
  }
  getModuleResolver() {
    let e = this.cachedModuleResolver;
    return null === e && (e = new ApiResolver("module"), this.cachedModuleResolver = e), 
    e;
  }
  getObjcResolver() {
    let e = this.cachedObjcResolver;
    if (null === e) {
      try {
        e = new ApiResolver("objc");
      } catch (e) {
        throw new Error("Objective-C runtime is not available");
      }
      this.cachedObjcResolver = e;
    }
    return e;
  }
  getSwiftResolver() {
    let e = this.cachedSwiftResolver;
    if (null === e) {
      try {
        e = new ApiResolver("swift");
      } catch (e) {
        throw new Error("Swift runtime is not available");
      }
      this.cachedSwiftResolver = e;
    }
    return e;
  }
}

async function t(e) {
  const t = [], {type: n, flavor: a, baseId: o} = e, r = e.scopes.slice().map((({name: e, members: t}) => ({
    name: e,
    members: t.slice()
  })));
  let i = o;
  do {
    const e = [], o = {
      type: n,
      flavor: a,
      baseId: i,
      scopes: e
    };
    let c = 0;
    for (const {name: t, members: s} of r) {
      const n = [];
      e.push({
        name: t,
        members: n
      });
      let a = !1;
      for (const e of s) if (n.push(e), c++, 1e3 === c) {
        a = !0;
        break;
      }
      if (s.splice(0, n.length), a) break;
    }
    for (;0 !== r.length && 0 === r[0].members.length; ) r.splice(0, 1);
    send(o);
    const l = await s(`reply:${i}`);
    t.push(...l.scripts), i += c;
  } while (0 !== r.length);
  return {
    scripts: t
  };
}

function s(e) {
  return new Promise((t => {
    recv(e, (e => {
      t(e);
    }));
  }));
}

function n(e) {
  const [t, s] = e.name.split("!").slice(-2);
  return [ "c", t, s ];
}

function a(e) {
  const {name: t} = e, [s, n] = t.substr(2, t.length - 3).split(" ", 2);
  return [ "objc", s, [ n, t ] ];
}

function o(e) {
  const {name: t} = e, [s, n] = t.split("!", 2);
  return [ "swift", s, n ];
}

function r(e) {
  const t = DebugSymbol.fromAddress(e);
  return [ "c", t.moduleName ?? "", t.name ];
}

function i(e) {
  const t = e.split("!", 2);
  let s, n;
  return 1 === t.length ? (s = "*", n = t[0]) : (s = "" === t[0] ? "*" : t[0], n = "" === t[1] ? "*" : t[1]), 
  {
    module: s,
    function: n
  };
}

function c(e) {
  const t = e.split("!", 2);
  return {
    module: t[0],
    offset: parseInt(t[1], 16)
  };
}

function l(e) {
  return {
    loader: e.loader,
    classes: new Map(e.classes.map((e => [ e.name, d(e) ])))
  };
}

function d(e) {
  return {
    methods: new Map(e.methods.map((e => [ u(e), e ])))
  };
}

function u(e) {
  const t = e.indexOf("(");
  return -1 === t ? e : e.substr(0, t);
}

function h(e, t) {
  for (const s of e) if (t(s)) return s;
}

function f() {}

const v = new e;

rpc.exports = {
  init: v.init.bind(v),
  dispose: v.dispose.bind(v),
  update: v.update.bind(v),
  stageTargets: v.stageTargets.bind(v),
  commitTargets: v.commitTargets.bind(v)
};

}).call(this)}).call(this,typeof global !== "undefined" ? global : typeof self !== "undefined" ? self : typeof window !== "undefined" ? window : {})

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJhZ2VudC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTs7OztBQ0FBLE1BQU07RUFBTixXQUFBO0lBQ1ksS0FBQSxXQUFXLElBQUksS0FDZixLQUFBLG9CQUE2QyxNQUM3QyxLQUFBLGFBQWEsSUFBSTtJQUNqQixLQUFBLGFBQXlCLElBQ3pCLEtBQUEsU0FBUyxHQUNULEtBQUEsVUFBVSxLQUFLLE9BRWYsS0FBQSxnQkFBOEI7SUFDOUIsS0FBQSxhQUFrQixNQUVsQixLQUFBLHVCQUEyQyxNQUMzQyxLQUFBLHFCQUF5QztJQUN6QyxLQUFBLHNCQUEwQyxNQWdwQjFDLEtBQUEsUUFBUTtNQU1aLElBTHdCLFNBQXBCLEtBQUssZUFDTCxhQUFhLEtBQUssYUFDbEIsS0FBSyxhQUFhO01BR1ksTUFBOUIsS0FBSyxjQUFjLFFBQ25CO01BR0osTUFBTSxJQUFTLEtBQUs7TUFDcEIsS0FBSyxnQkFBZ0IsSUFFckIsS0FBSztRQUNELE1BQU07UUFDTjs7QUFDRjtBQXFDVjtFQW5zQkksSUFBQSxDQUFLLEdBQWMsR0FBNkIsR0FBMkI7SUFDdkUsTUFBTSxJQUFJO0lBQ1YsRUFBRSxRQUFRLEdBQ1YsRUFBRSxhQUFhLEdBQ2YsRUFBRSxRQUFRLEtBQUssWUFDZixFQUFFLGdCQUFnQixLQUFLO0lBRXZCLEtBQUssTUFBTSxLQUFVLEdBQ2pCO09BQ0ksR0FBSSxNQUFNLEVBQU87TUFDbkIsT0FBTztNQUNMLE1BQU0sSUFBSSxNQUFNLGtCQUFrQixFQUFPLGFBQWEsRUFBRTs7SUFJaEUsS0FBSyxNQUFNLEdBQU0sT0FBTTtNQUNuQixLQUFLO1FBQ0QsTUFBTTtRQUNOLFNBQVMsRUFBRTs7QUFDYjtBQUVWO0VBRUEsT0FBQTtJQUNJLEtBQUs7QUFDVDtFQUVBLE1BQUEsQ0FBTyxHQUFtQixHQUFjO0lBQ3BDLE1BQU0sSUFBVSxLQUFLLFNBQVMsSUFBSTtJQUNsQyxTQUFnQixNQUFaLEdBQ0Es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
