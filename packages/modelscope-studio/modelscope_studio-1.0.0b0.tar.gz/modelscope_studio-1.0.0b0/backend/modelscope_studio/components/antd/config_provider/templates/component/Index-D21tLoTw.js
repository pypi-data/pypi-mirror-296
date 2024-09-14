async function M() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(t) {
  return await M(), t().then((e) => e.default);
}
function P() {
}
function B(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function H(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return P;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function b(t) {
  let e;
  return H(t, (o) => e = o)(), e;
}
const g = [];
function m(t, e = P) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (B(t, c) && (t = c, o)) {
      const a = !g.length;
      for (const u of n)
        u[1](), g.push(u, t);
      if (a) {
        for (let u = 0; u < g.length; u += 2)
          g[u][0](g[u + 1]);
        g.length = 0;
      }
    }
  }
  function s(c) {
    i(c(t));
  }
  function l(c, a = P) {
    const u = [c, a];
    return n.add(u), n.size === 1 && (o = e(i, s) || P), c(t), () => {
      n.delete(u), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
const {
  getContext: j,
  setContext: z
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function L() {
  const t = m({});
  return z(J, t);
}
const Q = "$$ms-gr-antd-context-key";
function U(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = X(), o = Y({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((a) => {
    o.slotKey.set(a);
  }), W();
  const n = j(Q), i = ((c = b(n)) == null ? void 0 : c.as_item) || t.as_item, s = n ? i ? b(n)[i] : b(n) : {}, l = m({
    ...t,
    ...s
  });
  return n ? (n.subscribe((a) => {
    const {
      as_item: u
    } = b(l);
    u && (a = a[u]), l.update((d) => ({
      ...d,
      ...a
    }));
  }), [l, (a) => {
    const u = a.as_item ? b(n)[a.as_item] : b(n);
    return l.set({
      ...a,
      ...u
    });
  }]) : [l, (a) => {
    l.set(a);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function W() {
  z(A, m(void 0));
}
function X() {
  return j(A);
}
const E = "$$ms-gr-antd-component-slot-context-key";
function Y({
  slot: t,
  index: e,
  subIndex: o
}) {
  return z(E, {
    slotKey: m(t),
    slotIndex: m(e),
    subSlotIndex: m(o)
  });
}
function Ce() {
  return j(E);
}
var ve = typeof globalThis < "u" ? globalThis : typeof window < "u" ? window : typeof global < "u" ? global : typeof self < "u" ? self : {};
function Z(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var R = {
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
    function o() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (s = i(s, n(c)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return o.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var c in s)
        e.call(s, c) && s[c] && (l = i(l, c));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(R);
var $ = R.exports;
const q = /* @__PURE__ */ Z($), {
  SvelteComponent: ee,
  assign: te,
  check_outros: ne,
  component_subscribe: x,
  create_component: se,
  create_slot: oe,
  destroy_component: ie,
  detach: T,
  empty: D,
  flush: _,
  get_all_dirty_from_scope: le,
  get_slot_changes: re,
  get_spread_object: ce,
  get_spread_update: ue,
  group_outros: ae,
  handle_promise: fe,
  init: _e,
  insert: F,
  mount_component: me,
  noop: f,
  safe_not_equal: de,
  transition_in: p,
  transition_out: h,
  update_await_block_branch: be,
  update_slot_base: ge
} = window.__gradio__svelte__internal;
function O(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: we,
    then: he,
    catch: pe,
    value: 18,
    blocks: [, , ,]
  };
  return fe(
    /*AwaitedConfigProvider*/
    t[2],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(i, s) {
      F(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, be(n, t, s);
    },
    i(i) {
      o || (p(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        h(l);
      }
      o = !1;
    },
    d(i) {
      i && T(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function pe(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function he(t) {
  let e, o;
  const n = [
    {
      className: q(
        "ms-gr-antd-config-provider",
        /*$mergedProps*/
        t[0].elem_classes
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    /*$mergedProps*/
    t[0].props,
    {
      slots: (
        /*$slots*/
        t[1]
      )
    },
    {
      theme_mode: (
        /*$mergedProps*/
        t[0].gradio.theme
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ye]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = te(i, n[s]);
  return e = new /*ConfigProvider*/
  t[18]({
    props: i
  }), {
    c() {
      se(e.$$.fragment);
    },
    m(s, l) {
      me(e, s, l), o = !0;
    },
    p(s, l) {
      const c = l & /*$mergedProps, $slots*/
      3 ? ue(n, [l & /*$mergedProps*/
      1 && {
        className: q(
          "ms-gr-antd-config-provider",
          /*$mergedProps*/
          s[0].elem_classes
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && ce(
        /*$mergedProps*/
        s[0].props
      ), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }, l & /*$mergedProps*/
      1 && {
        theme_mode: (
          /*$mergedProps*/
          s[0].gradio.theme
        )
      }]) : {};
      l & /*$$scope*/
      65536 && (c.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(c);
    },
    i(s) {
      o || (p(e.$$.fragment, s), o = !0);
    },
    o(s) {
      h(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ie(e, s);
    }
  };
}
function ye(t) {
  let e;
  const o = (
    /*#slots*/
    t[15].default
  ), n = oe(
    o,
    t,
    /*$$scope*/
    t[16],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, s) {
      n && n.m(i, s), e = !0;
    },
    p(i, s) {
      n && n.p && (!e || s & /*$$scope*/
      65536) && ge(
        n,
        o,
        i,
        /*$$scope*/
        i[16],
        e ? re(
          o,
          /*$$scope*/
          i[16],
          s,
          null
        ) : le(
          /*$$scope*/
          i[16]
        ),
        null
      );
    },
    i(i) {
      e || (p(n, i), e = !0);
    },
    o(i) {
      h(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function we(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function ke(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && O(t)
  );
  return {
    c() {
      n && n.c(), e = D();
    },
    m(i, s) {
      n && n.m(i, s), F(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && p(n, 1)) : (n = O(i), n.c(), p(n, 1), n.m(e.parentNode, e)) : n && (ae(), h(n, 1, 1, () => {
        n = null;
      }), ne());
    },
    i(i) {
      o || (p(n), o = !0);
    },
    o(i) {
      h(n), o = !1;
    },
    d(i) {
      i && T(e), n && n.d(i);
    }
  };
}
function Se(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: c
  } = e;
  const a = V(() => import("./config-provider-CtYoo49W.js"));
  let {
    gradio: u
  } = e, {
    props: d = {}
  } = e;
  const K = m(d);
  x(t, K, (r) => o(14, n = r));
  let {
    as_item: y
  } = e, {
    visible: w = !0
  } = e, {
    elem_id: k = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: C = {}
  } = e, {
    _internal: v = {}
  } = e;
  const [I, G] = U({
    gradio: u,
    props: n,
    visible: w,
    _internal: v,
    elem_id: k,
    elem_classes: S,
    elem_style: C,
    as_item: y
  });
  x(t, I, (r) => o(0, i = r));
  const N = L();
  return x(t, N, (r) => o(1, s = r)), t.$$set = (r) => {
    "gradio" in r && o(6, u = r.gradio), "props" in r && o(7, d = r.props), "as_item" in r && o(8, y = r.as_item), "visible" in r && o(9, w = r.visible), "elem_id" in r && o(10, k = r.elem_id), "elem_classes" in r && o(11, S = r.elem_classes), "elem_style" in r && o(12, C = r.elem_style), "_internal" in r && o(13, v = r._internal), "$$scope" in r && o(16, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && K.update((r) => ({
      ...r,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, visible, _internal, elem_id, elem_classes, elem_style, as_item*/
    32576 && G({
      gradio: u,
      props: n,
      visible: w,
      _internal: v,
      elem_id: k,
      elem_classes: S,
      elem_style: C,
      as_item: y
    });
  }, [i, s, a, K, I, N, u, d, y, w, k, S, C, v, n, l, c];
}
class Pe extends ee {
  constructor(e) {
    super(), _e(this, e, Se, ke, de, {
      gradio: 6,
      props: 7,
      as_item: 8,
      visible: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12,
      _internal: 13
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), _();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[9];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
}
export {
  Pe as I,
  Z as a,
  ve as c,
  Ce as g,
  m as w
};
