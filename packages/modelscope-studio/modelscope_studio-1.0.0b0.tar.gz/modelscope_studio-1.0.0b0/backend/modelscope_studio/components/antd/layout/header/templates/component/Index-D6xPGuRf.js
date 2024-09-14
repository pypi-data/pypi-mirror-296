async function G() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((s) => {
    window.ms_globals.initialize = () => {
      s();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(s) {
  return await G(), s().then((e) => e.default);
}
function O(s) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = s;
  return Object.keys(i).reduce((o, t) => {
    const l = t.match(/bind_(.+)_event/);
    if (l) {
      const r = l[1], a = r.split("_"), _ = (...f) => {
        const b = f.map((u) => f && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return e.dispatch(r.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (a.length > 1) {
        let f = {
          ...n.props[a[0]] || {}
        };
        o[a[0]] = f;
        for (let u = 1; u < a.length - 1; u++) {
          const g = {
            ...n.props[a[u]] || {}
          };
          f[a[u]] = g, f = g;
        }
        const b = a[a.length - 1];
        return f[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, o;
      }
      const d = a[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function P() {
}
function J(s, e) {
  return s != s ? e == e : s !== e || s && typeof s == "object" || typeof s == "function";
}
function Q(s, ...e) {
  if (s == null) {
    for (const n of e)
      n(void 0);
    return P;
  }
  const i = s.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(s) {
  let e;
  return Q(s, (i) => e = i)(), e;
}
const w = [];
function h(s, e = P) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(r) {
    if (J(s, r) && (s = r, i)) {
      const a = !w.length;
      for (const _ of n)
        _[1](), w.push(_, s);
      if (a) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function t(r) {
    o(r(s));
  }
  function l(r, a = P) {
    const _ = [r, a];
    return n.add(_), n.size === 1 && (i = e(o, t) || P), r(s), () => {
      n.delete(_), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: t,
    subscribe: l
  };
}
const {
  getContext: q,
  setContext: z
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const s = h({});
  return z(T, s);
}
const ee = "$$ms-gr-antd-context-key";
function te(s) {
  var r;
  if (!Reflect.has(s, "as_item") || !Reflect.has(s, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = se(), i = oe({
    slot: void 0,
    index: s._internal.index,
    subIndex: s._internal.subIndex
  });
  e && e.subscribe((a) => {
    i.slotKey.set(a);
  }), ne();
  const n = q(ee), o = ((r = y(n)) == null ? void 0 : r.as_item) || s.as_item, t = n ? o ? y(n)[o] : y(n) : {}, l = h({
    ...s,
    ...t
  });
  return n ? (n.subscribe((a) => {
    const {
      as_item: _
    } = y(l);
    _ && (a = a[_]), l.update((d) => ({
      ...d,
      ...a
    }));
  }), [l, (a) => {
    const _ = a.as_item ? y(n)[a.as_item] : y(n);
    return l.set({
      ...a,
      ..._
    });
  }]) : [l, (a) => {
    l.set(a);
  }];
}
const R = "$$ms-gr-antd-slot-key";
function ne() {
  z(R, h(void 0));
}
function se() {
  return q(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function oe({
  slot: s,
  index: e,
  subIndex: i
}) {
  return z(U, {
    slotKey: h(s),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function Me() {
  return q(U);
}
function ie(s) {
  return s && s.__esModule && Object.prototype.hasOwnProperty.call(s, "default") ? s.default : s;
}
var X = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(s) {
  (function() {
    var e = {}.hasOwnProperty;
    function i() {
      for (var t = "", l = 0; l < arguments.length; l++) {
        var r = arguments[l];
        r && (t = o(t, n(r)));
      }
      return t;
    }
    function n(t) {
      if (typeof t == "string" || typeof t == "number")
        return t;
      if (typeof t != "object")
        return "";
      if (Array.isArray(t))
        return i.apply(null, t);
      if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]"))
        return t.toString();
      var l = "";
      for (var r in t)
        e.call(t, r) && t[r] && (l = o(l, r));
      return l;
    }
    function o(t, l) {
      return l ? t ? t + " " + l : t + l : t;
    }
    s.exports ? (i.default = i, s.exports = i) : window.classNames = i;
  })();
})(X);
var le = X.exports;
const A = /* @__PURE__ */ ie(le), {
  SvelteComponent: re,
  assign: ce,
  check_outros: ae,
  component_subscribe: j,
  create_component: ue,
  create_slot: _e,
  destroy_component: fe,
  detach: Y,
  empty: D,
  flush: p,
  get_all_dirty_from_scope: me,
  get_slot_changes: de,
  get_spread_object: x,
  get_spread_update: pe,
  group_outros: be,
  handle_promise: ge,
  init: he,
  insert: F,
  mount_component: ye,
  noop: m,
  safe_not_equal: we,
  transition_in: k,
  transition_out: C,
  update_await_block_branch: ke,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function B(s) {
  let e, i, n = {
    ctx: s,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ve,
    then: Ke,
    catch: Se,
    value: 19,
    blocks: [, , ,]
  };
  return ge(
    /*AwaitedLayoutBase*/
    s[3],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(o, t) {
      F(o, e, t), n.block.m(o, n.anchor = t), n.mount = () => e.parentNode, n.anchor = e, i = !0;
    },
    p(o, t) {
      s = o, ke(n, s, t);
    },
    i(o) {
      i || (k(n.block), i = !0);
    },
    o(o) {
      for (let t = 0; t < 3; t += 1) {
        const l = n.blocks[t];
        C(l);
      }
      i = !1;
    },
    d(o) {
      o && Y(e), n.block.d(o), n.token = null, n = null;
    }
  };
}
function Se(s) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ke(s) {
  let e, i;
  const n = [
    {
      component: (
        /*component*/
        s[0]
      )
    },
    {
      style: (
        /*$mergedProps*/
        s[1].elem_style
      )
    },
    {
      className: A(
        /*$mergedProps*/
        s[1].elem_classes
      )
    },
    {
      id: (
        /*$mergedProps*/
        s[1].elem_id
      )
    },
    /*$mergedProps*/
    s[1].props,
    O(
      /*$mergedProps*/
      s[1]
    ),
    {
      slots: (
        /*$slots*/
        s[2]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [$e]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let t = 0; t < n.length; t += 1)
    o = ce(o, n[t]);
  return e = new /*LayoutBase*/
  s[19]({
    props: o
  }), {
    c() {
      ue(e.$$.fragment);
    },
    m(t, l) {
      ye(e, t, l), i = !0;
    },
    p(t, l) {
      const r = l & /*component, $mergedProps, $slots*/
      7 ? pe(n, [l & /*component*/
      1 && {
        component: (
          /*component*/
          t[0]
        )
      }, l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          t[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          t[1].elem_classes
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          t[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && x(
        /*$mergedProps*/
        t[1].props
      ), l & /*$mergedProps*/
      2 && x(O(
        /*$mergedProps*/
        t[1]
      )), l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          t[2]
        )
      }]) : {};
      l & /*$$scope*/
      131072 && (r.$$scope = {
        dirty: l,
        ctx: t
      }), e.$set(r);
    },
    i(t) {
      i || (k(e.$$.fragment, t), i = !0);
    },
    o(t) {
      C(e.$$.fragment, t), i = !1;
    },
    d(t) {
      fe(e, t);
    }
  };
}
function $e(s) {
  let e;
  const i = (
    /*#slots*/
    s[16].default
  ), n = _e(
    i,
    s,
    /*$$scope*/
    s[17],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, t) {
      n && n.m(o, t), e = !0;
    },
    p(o, t) {
      n && n.p && (!e || t & /*$$scope*/
      131072) && Ce(
        n,
        i,
        o,
        /*$$scope*/
        o[17],
        e ? de(
          i,
          /*$$scope*/
          o[17],
          t,
          null
        ) : me(
          /*$$scope*/
          o[17]
        ),
        null
      );
    },
    i(o) {
      e || (k(n, o), e = !0);
    },
    o(o) {
      C(n, o), e = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function ve(s) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Pe(s) {
  let e, i, n = (
    /*$mergedProps*/
    s[1].visible && B(s)
  );
  return {
    c() {
      n && n.c(), e = D();
    },
    m(o, t) {
      n && n.m(o, t), F(o, e, t), i = !0;
    },
    p(o, [t]) {
      /*$mergedProps*/
      o[1].visible ? n ? (n.p(o, t), t & /*$mergedProps*/
      2 && k(n, 1)) : (n = B(o), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (be(), C(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(o) {
      i || (k(n), i = !0);
    },
    o(o) {
      C(n), i = !1;
    },
    d(o) {
      o && Y(e), n && n.d(o);
    }
  };
}
function je(s, e, i) {
  let n, o, t, {
    $$slots: l = {},
    $$scope: r
  } = e;
  const a = H(() => import("./layout.base-DpUL35eV.js"));
  let {
    component: _
  } = e, {
    gradio: d = {}
  } = e, {
    props: f = {}
  } = e;
  const b = h(f);
  j(s, b, (c) => i(15, n = c));
  let {
    _internal: u = {}
  } = e, {
    as_item: g = void 0
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: $ = []
  } = e, {
    elem_style: v = {}
  } = e;
  const [I, Z] = te({
    gradio: d,
    props: n,
    _internal: u,
    visible: S,
    elem_id: K,
    elem_classes: $,
    elem_style: v,
    as_item: g
  });
  j(s, I, (c) => i(1, o = c));
  const E = W();
  return j(s, E, (c) => i(2, t = c)), s.$$set = (c) => {
    "component" in c && i(0, _ = c.component), "gradio" in c && i(7, d = c.gradio), "props" in c && i(8, f = c.props), "_internal" in c && i(9, u = c._internal), "as_item" in c && i(10, g = c.as_item), "visible" in c && i(11, S = c.visible), "elem_id" in c && i(12, K = c.elem_id), "elem_classes" in c && i(13, $ = c.elem_classes), "elem_style" in c && i(14, v = c.elem_style), "$$scope" in c && i(17, r = c.$$scope);
  }, s.$$.update = () => {
    s.$$.dirty & /*props*/
    256 && b.update((c) => ({
      ...c,
      ...f
    })), s.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    65152 && Z({
      gradio: d,
      props: n,
      _internal: u,
      visible: S,
      elem_id: K,
      elem_classes: $,
      elem_style: v,
      as_item: g
    });
  }, [_, o, t, a, b, I, E, d, f, u, g, S, K, $, v, n, l, r];
}
class Ne extends re {
  constructor(e) {
    super(), he(this, e, je, Pe, we, {
      component: 0,
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get component() {
    return this.$$.ctx[0];
  }
  set component(e) {
    this.$$set({
      component: e
    }), p();
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), p();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
const {
  SvelteComponent: qe,
  assign: N,
  create_component: ze,
  create_slot: Ie,
  destroy_component: Ee,
  exclude_internal_props: L,
  get_all_dirty_from_scope: Oe,
  get_slot_changes: Ae,
  get_spread_object: xe,
  get_spread_update: Be,
  init: Le,
  mount_component: Re,
  safe_not_equal: Ue,
  transition_in: M,
  transition_out: V,
  update_slot_base: Xe
} = window.__gradio__svelte__internal;
function Ye(s) {
  let e;
  const i = (
    /*#slots*/
    s[1].default
  ), n = Ie(
    i,
    s,
    /*$$scope*/
    s[2],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, t) {
      n && n.m(o, t), e = !0;
    },
    p(o, t) {
      n && n.p && (!e || t & /*$$scope*/
      4) && Xe(
        n,
        i,
        o,
        /*$$scope*/
        o[2],
        e ? Ae(
          i,
          /*$$scope*/
          o[2],
          t,
          null
        ) : Oe(
          /*$$scope*/
          o[2]
        ),
        null
      );
    },
    i(o) {
      e || (M(n, o), e = !0);
    },
    o(o) {
      V(n, o), e = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function De(s) {
  let e, i;
  const n = [
    /*$$props*/
    s[0],
    {
      component: "header"
    }
  ];
  let o = {
    $$slots: {
      default: [Ye]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let t = 0; t < n.length; t += 1)
    o = N(o, n[t]);
  return e = new Ne({
    props: o
  }), {
    c() {
      ze(e.$$.fragment);
    },
    m(t, l) {
      Re(e, t, l), i = !0;
    },
    p(t, [l]) {
      const r = l & /*$$props*/
      1 ? Be(n, [xe(
        /*$$props*/
        t[0]
      ), n[1]]) : {};
      l & /*$$scope*/
      4 && (r.$$scope = {
        dirty: l,
        ctx: t
      }), e.$set(r);
    },
    i(t) {
      i || (M(e.$$.fragment, t), i = !0);
    },
    o(t) {
      V(e.$$.fragment, t), i = !1;
    },
    d(t) {
      Ee(e, t);
    }
  };
}
function Fe(s, e, i) {
  let {
    $$slots: n = {},
    $$scope: o
  } = e;
  return s.$$set = (t) => {
    i(0, e = N(N({}, e), L(t))), "$$scope" in t && i(2, o = t.$$scope);
  }, e = L(e), [e, n, o];
}
class Ve extends qe {
  constructor(e) {
    super(), Le(this, e, Fe, De, Ue, {});
  }
}
export {
  Ve as I,
  A as c,
  Me as g,
  h as w
};
