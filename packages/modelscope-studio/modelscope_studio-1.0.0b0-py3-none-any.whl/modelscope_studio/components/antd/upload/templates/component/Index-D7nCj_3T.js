async function J() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function Q(t) {
  return await J(), t().then((e) => e.default);
}
function F(t) {
  const {
    gradio: e,
    _internal: n,
    ...s
  } = t;
  return Object.keys(n).reduce((o, i) => {
    const l = i.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], a = u.split("_"), _ = (...m) => {
        const h = m.map((c) => m && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return e.dispatch(u.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: h,
          component: s
        });
      };
      if (a.length > 1) {
        let m = {
          ...s.props[a[0]] || {}
        };
        o[a[0]] = m;
        for (let c = 1; c < a.length - 1; c++) {
          const g = {
            ...s.props[a[c]] || {}
          };
          m[a[c]] = g, m = g;
        }
        const h = a[a.length - 1];
        return m[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = _, o;
      }
      const p = a[0];
      o[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function O() {
}
function $(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function ee(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return O;
  }
  const n = t.subscribe(...e);
  return n.unsubscribe ? () => n.unsubscribe() : n;
}
function v(t) {
  let e;
  return ee(t, (n) => e = n)(), e;
}
const C = [];
function w(t, e = O) {
  let n;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if ($(t, u) && (t = u, n)) {
      const a = !C.length;
      for (const _ of s)
        _[1](), C.push(_, t);
      if (a) {
        for (let _ = 0; _ < C.length; _ += 2)
          C[_][0](C[_ + 1]);
        C.length = 0;
      }
    }
  }
  function i(u) {
    o(u(t));
  }
  function l(u, a = O) {
    const _ = [u, a];
    return s.add(_), s.size === 1 && (n = e(o, i) || O), u(t), () => {
      s.delete(_), s.size === 0 && n && (n(), n = null);
    };
  }
  return {
    set: o,
    update: i,
    subscribe: l
  };
}
const {
  getContext: E,
  setContext: L
} = window.__gradio__svelte__internal, te = "$$ms-gr-antd-slots-key";
function ne() {
  const t = w({});
  return L(te, t);
}
const se = "$$ms-gr-antd-context-key";
function ie(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = le(), n = re({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((a) => {
    n.slotKey.set(a);
  }), oe();
  const s = E(se), o = ((u = v(s)) == null ? void 0 : u.as_item) || t.as_item, i = s ? o ? v(s)[o] : v(s) : {}, l = w({
    ...t,
    ...i
  });
  return s ? (s.subscribe((a) => {
    const {
      as_item: _
    } = v(l);
    _ && (a = a[_]), l.update((p) => ({
      ...p,
      ...a
    }));
  }), [l, (a) => {
    const _ = a.as_item ? v(s)[a.as_item] : v(s);
    return l.set({
      ...a,
      ..._
    });
  }]) : [l, (a) => {
    l.set(a);
  }];
}
const V = "$$ms-gr-antd-slot-key";
function oe() {
  L(V, w(void 0));
}
function le() {
  return E(V);
}
const W = "$$ms-gr-antd-component-slot-context-key";
function re({
  slot: t,
  index: e,
  subIndex: n
}) {
  return L(W, {
    slotKey: w(t),
    slotIndex: w(e),
    subSlotIndex: w(n)
  });
}
function Te() {
  return E(W);
}
var ae = Object.defineProperty, ue = (t, e, n) => e in t ? ae(t, e, {
  enumerable: !0,
  configurable: !0,
  writable: !0,
  value: n
}) : t[e] = n, b = (t, e, n) => (ue(t, typeof e != "symbol" ? e + "" : e, n), n), j = (t, e, n) => {
  if (!e.has(t)) throw TypeError("Cannot " + n);
}, S = (t, e, n) => (j(t, e, "read from private field"), n ? n.call(t) : e.get(t)), ce = (t, e, n) => {
  if (e.has(t)) throw TypeError("Cannot add the same private member more than once");
  e instanceof WeakSet ? e.add(t) : e.set(t, n);
}, _e = (t, e, n, s) => (j(t, e, "write to private field"), e.set(t, n), n), y;
new Intl.Collator(0, {
  numeric: 1
}).compare;
async function fe(t, e) {
  return t.map((n) => new me({
    path: n.name,
    orig_name: n.name,
    blob: n,
    size: n.size,
    mime_type: n.type,
    is_stream: e
  }));
}
class me {
  constructor({
    path: e,
    url: n,
    orig_name: s,
    size: o,
    blob: i,
    is_stream: l,
    mime_type: u,
    alt_text: a
  }) {
    b(this, "path"), b(this, "url"), b(this, "orig_name"), b(this, "size"), b(this, "blob"), b(this, "is_stream"), b(this, "mime_type"), b(this, "alt_text"), b(this, "meta", {
      _type: "gradio.FileData"
    }), this.path = e, this.url = n, this.orig_name = s, this.size = o, this.blob = n ? void 0 : i, this.is_stream = l, this.mime_type = u, this.alt_text = a;
  }
}
typeof process < "u" && process.versions && process.versions.node;
class De extends TransformStream {
  /** Constructs a new instance. */
  constructor(e = {
    allowCR: !1
  }) {
    super({
      transform: (n, s) => {
        for (n = S(this, y) + n; ; ) {
          const o = n.indexOf(`
`), i = e.allowCR ? n.indexOf("\r") : -1;
          if (i !== -1 && i !== n.length - 1 && (o === -1 || o - 1 > i)) {
            s.enqueue(n.slice(0, i)), n = n.slice(i + 1);
            continue;
          }
          if (o === -1) break;
          const l = n[o - 1] === "\r" ? o - 1 : o;
          s.enqueue(n.slice(0, l)), n = n.slice(o + 1);
        }
        _e(this, y, n);
      },
      flush: (n) => {
        if (S(this, y) === "") return;
        const s = e.allowCR && S(this, y).endsWith("\r") ? S(this, y).slice(0, -1) : S(this, y);
        n.enqueue(s);
      }
    }), ce(this, y, "");
  }
}
y = /* @__PURE__ */ new WeakMap();
function de(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var M = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(t) {
  (function() {
    var e = {}.hasOwnProperty;
    function n() {
      for (var i = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (i = o(i, s(u)));
      }
      return i;
    }
    function s(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return n.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var l = "";
      for (var u in i)
        e.call(i, u) && i[u] && (l = o(l, u));
      return l;
    }
    function o(i, l) {
      return l ? i ? i + " " + l : i + l : i;
    }
    t.exports ? (n.default = n, t.exports = n) : window.classNames = n;
  })();
})(M);
var pe = M.exports;
const T = /* @__PURE__ */ de(pe), {
  SvelteComponent: he,
  assign: be,
  check_outros: ge,
  component_subscribe: q,
  create_component: ye,
  create_slot: we,
  destroy_component: ve,
  detach: X,
  empty: Y,
  flush: d,
  get_all_dirty_from_scope: Ce,
  get_slot_changes: ke,
  get_spread_object: D,
  get_spread_update: Se,
  group_outros: Ke,
  handle_promise: Pe,
  init: xe,
  insert: G,
  mount_component: ze,
  noop: f,
  safe_not_equal: Ie,
  transition_in: k,
  transition_out: K,
  update_await_block_branch: Ne,
  update_slot_base: Oe
} = window.__gradio__svelte__internal;
function U(t) {
  let e, n, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ae,
    then: Ee,
    catch: qe,
    value: 22,
    blocks: [, , ,]
  };
  return Pe(
    /*AwaitedUpload*/
    t[5],
    s
  ), {
    c() {
      e = Y(), s.block.c();
    },
    m(o, i) {
      G(o, e, i), s.block.m(o, s.anchor = i), s.mount = () => e.parentNode, s.anchor = e, n = !0;
    },
    p(o, i) {
      t = o, Ne(s, t, i);
    },
    i(o) {
      n || (k(s.block), n = !0);
    },
    o(o) {
      for (let i = 0; i < 3; i += 1) {
        const l = s.blocks[i];
        K(l);
      }
      n = !1;
    },
    d(o) {
      o && X(e), s.block.d(o), s.token = null, s = null;
    }
  };
}
function qe(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ee(t) {
  let e, n;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[3].elem_style
      )
    },
    {
      className: T(
        /*$mergedProps*/
        t[3].elem_classes,
        "ms-gr-antd-upload"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[3].elem_id
      )
    },
    {
      fileList: (
        /*$mergedProps*/
        t[3].value
      )
    },
    /*$mergedProps*/
    t[3].props,
    F(
      /*$mergedProps*/
      t[3]
    ),
    {
      slots: (
        /*$slots*/
        t[4]
      )
    },
    {
      onValueChange: (
        /*func*/
        t[18]
      )
    },
    {
      upload: (
        /*func_1*/
        t[19]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Le]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let i = 0; i < s.length; i += 1)
    o = be(o, s[i]);
  return e = new /*Upload*/
  t[22]({
    props: o
  }), {
    c() {
      ye(e.$$.fragment);
    },
    m(i, l) {
      ze(e, i, l), n = !0;
    },
    p(i, l) {
      const u = l & /*$mergedProps, $slots, value, gradio, root*/
      31 ? Se(s, [l & /*$mergedProps*/
      8 && {
        style: (
          /*$mergedProps*/
          i[3].elem_style
        )
      }, l & /*$mergedProps*/
      8 && {
        className: T(
          /*$mergedProps*/
          i[3].elem_classes,
          "ms-gr-antd-upload"
        )
      }, l & /*$mergedProps*/
      8 && {
        id: (
          /*$mergedProps*/
          i[3].elem_id
        )
      }, l & /*$mergedProps*/
      8 && {
        fileList: (
          /*$mergedProps*/
          i[3].value
        )
      }, l & /*$mergedProps*/
      8 && D(
        /*$mergedProps*/
        i[3].props
      ), l & /*$mergedProps*/
      8 && D(F(
        /*$mergedProps*/
        i[3]
      )), l & /*$slots*/
      16 && {
        slots: (
          /*$slots*/
          i[4]
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          i[18]
        )
      }, l & /*gradio, root*/
      6 && {
        upload: (
          /*func_1*/
          i[19]
        )
      }]) : {};
      l & /*$$scope*/
      1048576 && (u.$$scope = {
        dirty: l,
        ctx: i
      }), e.$set(u);
    },
    i(i) {
      n || (k(e.$$.fragment, i), n = !0);
    },
    o(i) {
      K(e.$$.fragment, i), n = !1;
    },
    d(i) {
      ve(e, i);
    }
  };
}
function Le(t) {
  let e;
  const n = (
    /*#slots*/
    t[17].default
  ), s = we(
    n,
    t,
    /*$$scope*/
    t[20],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, i) {
      s && s.m(o, i), e = !0;
    },
    p(o, i) {
      s && s.p && (!e || i & /*$$scope*/
      1048576) && Oe(
        s,
        n,
        o,
        /*$$scope*/
        o[20],
        e ? ke(
          n,
          /*$$scope*/
          o[20],
          i,
          null
        ) : Ce(
          /*$$scope*/
          o[20]
        ),
        null
      );
    },
    i(o) {
      e || (k(s, o), e = !0);
    },
    o(o) {
      K(s, o), e = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ae(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Re(t) {
  let e, n, s = (
    /*$mergedProps*/
    t[3].visible && U(t)
  );
  return {
    c() {
      s && s.c(), e = Y();
    },
    m(o, i) {
      s && s.m(o, i), G(o, e, i), n = !0;
    },
    p(o, [i]) {
      /*$mergedProps*/
      o[3].visible ? s ? (s.p(o, i), i & /*$mergedProps*/
      8 && k(s, 1)) : (s = U(o), s.c(), k(s, 1), s.m(e.parentNode, e)) : s && (Ke(), K(s, 1, 1, () => {
        s = null;
      }), ge());
    },
    i(o) {
      n || (k(s), n = !0);
    },
    o(o) {
      K(s), n = !1;
    },
    d(o) {
      o && X(e), s && s.d(o);
    }
  };
}
function Fe(t, e, n) {
  let s, o, i, {
    $$slots: l = {},
    $$scope: u
  } = e;
  const a = Q(() => import("./upload-BheF7GVi.js"));
  let {
    gradio: _
  } = e, {
    props: p = {}
  } = e;
  const m = w(p);
  q(t, m, (r) => n(16, s = r));
  let {
    _internal: h
  } = e, {
    root: c
  } = e, {
    value: g = []
  } = e, {
    as_item: P
  } = e, {
    visible: x = !0
  } = e, {
    elem_id: z = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: N = {}
  } = e;
  const [A, Z] = ie({
    gradio: _,
    props: s,
    _internal: h,
    value: g,
    visible: x,
    elem_id: z,
    elem_classes: I,
    elem_style: N,
    as_item: P
  });
  q(t, A, (r) => n(3, o = r));
  const R = ne();
  q(t, R, (r) => n(4, i = r));
  const B = (r) => {
    n(0, g = r);
  }, H = async (r) => await _.client.upload(await fe(r), c) || [];
  return t.$$set = (r) => {
    "gradio" in r && n(1, _ = r.gradio), "props" in r && n(9, p = r.props), "_internal" in r && n(10, h = r._internal), "root" in r && n(2, c = r.root), "value" in r && n(0, g = r.value), "as_item" in r && n(11, P = r.as_item), "visible" in r && n(12, x = r.visible), "elem_id" in r && n(13, z = r.elem_id), "elem_classes" in r && n(14, I = r.elem_classes), "elem_style" in r && n(15, N = r.elem_style), "$$scope" in r && n(20, u = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && m.update((r) => ({
      ...r,
      ...p
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, value, visible, elem_id, elem_classes, elem_style, as_item*/
    130051 && Z({
      gradio: _,
      props: s,
      _internal: h,
      value: g,
      visible: x,
      elem_id: z,
      elem_classes: I,
      elem_style: N,
      as_item: P
    });
  }, [g, _, c, o, i, a, m, A, R, p, h, P, x, z, I, N, s, l, B, H, u];
}
class Ue extends he {
  constructor(e) {
    super(), xe(this, e, Fe, Re, Ie, {
      gradio: 1,
      props: 9,
      _internal: 10,
      root: 2,
      value: 0,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), d();
  }
  get root() {
    return this.$$.ctx[2];
  }
  set root(e) {
    this.$$set({
      root: e
    }), d();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  Ue as I,
  Te as g,
  w
};
