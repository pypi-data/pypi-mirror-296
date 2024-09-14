async function Q() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((n) => {
    window.ms_globals.initialize = () => {
      n();
    };
  })), await window.ms_globals.initializePromise;
}
async function W(n) {
  return await Q(), n().then((e) => e.default);
}
function R(n) {
  const {
    gradio: e,
    _internal: o,
    ...t
  } = n;
  return Object.keys(o).reduce((l, s) => {
    const i = s.match(/bind_(.+)_event/);
    if (i) {
      const c = i[1], r = c.split("_"), u = (...m) => {
        const b = m.map((_) => m && typeof _ == "object" && (_.nativeEvent || _ instanceof Event) ? {
          type: _.type,
          detail: _.detail,
          timestamp: _.timeStamp,
          clientX: _.clientX,
          clientY: _.clientY,
          targetId: _.target.id,
          targetClassName: _.target.className,
          altKey: _.altKey,
          ctrlKey: _.ctrlKey,
          shiftKey: _.shiftKey,
          metaKey: _.metaKey
        } : _);
        return e.dispatch(c.replace(/[A-Z]/g, (_) => "_" + _.toLowerCase()), {
          payload: b,
          component: t
        });
      };
      if (r.length > 1) {
        let m = {
          ...t.props[r[0]] || {}
        };
        l[r[0]] = m;
        for (let _ = 1; _ < r.length - 1; _++) {
          const d = {
            ...t.props[r[_]] || {}
          };
          m[r[_]] = d, m = d;
        }
        const b = r[r.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = u, l;
      }
      const f = r[0];
      l[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = u;
    }
    return l;
  }, {});
}
function K() {
}
function ee(n) {
  return n();
}
function te(n) {
  n.forEach(ee);
}
function ne(n) {
  return typeof n == "function";
}
function se(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function F(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return K;
  }
  const o = n.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function C(n) {
  let e;
  return F(n, (o) => e = o)(), e;
}
const S = [];
function oe(n, e) {
  return {
    subscribe: y(n, e).subscribe
  };
}
function y(n, e = K) {
  let o;
  const t = /* @__PURE__ */ new Set();
  function l(c) {
    if (se(n, c) && (n = c, o)) {
      const r = !S.length;
      for (const u of t)
        u[1](), S.push(u, n);
      if (r) {
        for (let u = 0; u < S.length; u += 2)
          S[u][0](S[u + 1]);
        S.length = 0;
      }
    }
  }
  function s(c) {
    l(c(n));
  }
  function i(c, r = K) {
    const u = [c, r];
    return t.add(u), t.size === 1 && (o = e(l, s) || K), c(n), () => {
      t.delete(u), t.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: l,
    update: s,
    subscribe: i
  };
}
function tt(n, e, o) {
  const t = !Array.isArray(n), l = t ? [n] : n;
  if (!l.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = e.length < 2;
  return oe(o, (i, c) => {
    let r = !1;
    const u = [];
    let f = 0, m = K;
    const b = () => {
      if (f)
        return;
      m();
      const d = e(t ? u[0] : u, i, c);
      s ? i(d) : m = ne(d) ? d : K;
    }, _ = l.map((d, g) => F(d, (w) => {
      u[g] = w, f &= ~(1 << g), r && b();
    }, () => {
      f |= 1 << g;
    }));
    return r = !0, b(), function() {
      te(_), m(), r = !1;
    };
  });
}
const {
  getContext: I,
  setContext: A
} = window.__gradio__svelte__internal, le = "$$ms-gr-antd-slots-key";
function ie() {
  const n = y({});
  return A(le, n);
}
const re = "$$ms-gr-antd-context-key";
function ce(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ae(), o = _e({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), ue();
  const t = I(re), l = ((c = C(t)) == null ? void 0 : c.as_item) || n.as_item, s = t ? l ? C(t)[l] : C(t) : {}, i = y({
    ...n,
    ...s
  });
  return t ? (t.subscribe((r) => {
    const {
      as_item: u
    } = C(i);
    u && (r = r[u]), i.update((f) => ({
      ...f,
      ...r
    }));
  }), [i, (r) => {
    const u = r.as_item ? C(t)[r.as_item] : C(t);
    return i.set({
      ...r,
      ...u
    });
  }]) : [i, (r) => {
    i.set(r);
  }];
}
const L = "$$ms-gr-antd-slot-key";
function ue() {
  A(L, y(void 0));
}
function ae() {
  return I(L);
}
const M = "$$ms-gr-antd-component-slot-context-key";
function _e({
  slot: n,
  index: e,
  subIndex: o
}) {
  return A(M, {
    slotKey: y(n),
    slotIndex: y(e),
    subSlotIndex: y(o)
  });
}
function nt() {
  return I(M);
}
function fe(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var T = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var e = {}.hasOwnProperty;
    function o() {
      for (var s = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (s = l(s, t(c)));
      }
      return s;
    }
    function t(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return o.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var i = "";
      for (var c in s)
        e.call(s, c) && s[c] && (i = l(i, c));
      return i;
    }
    function l(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    n.exports ? (o.default = o, n.exports = o) : window.classNames = o;
  })();
})(T);
var me = T.exports;
const U = /* @__PURE__ */ fe(me), {
  SvelteComponent: de,
  assign: pe,
  check_outros: V,
  component_subscribe: q,
  create_component: be,
  create_slot: he,
  destroy_component: ge,
  detach: $,
  empty: O,
  flush: h,
  get_all_dirty_from_scope: ye,
  get_slot_changes: ve,
  get_spread_object: X,
  get_spread_update: ke,
  group_outros: Z,
  handle_promise: we,
  init: Ce,
  insert: E,
  mount_component: Se,
  noop: p,
  safe_not_equal: Ke,
  set_data: Pe,
  text: je,
  transition_in: v,
  transition_out: k,
  update_await_block_branch: Ne,
  update_slot_base: $e
} = window.__gradio__svelte__internal;
function Y(n) {
  let e, o, t = {
    ctx: n,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Oe,
    then: qe,
    catch: Ee,
    value: 20,
    blocks: [, , ,]
  };
  return we(
    /*AwaitedTypographyBase*/
    n[3],
    t
  ), {
    c() {
      e = O(), t.block.c();
    },
    m(l, s) {
      E(l, e, s), t.block.m(l, t.anchor = s), t.mount = () => e.parentNode, t.anchor = e, o = !0;
    },
    p(l, s) {
      n = l, Ne(t, n, s);
    },
    i(l) {
      o || (v(t.block), o = !0);
    },
    o(l) {
      for (let s = 0; s < 3; s += 1) {
        const i = t.blocks[s];
        k(i);
      }
      o = !1;
    },
    d(l) {
      l && $(e), t.block.d(l), t.token = null, t = null;
    }
  };
}
function Ee(n) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function qe(n) {
  let e, o;
  const t = [
    {
      component: (
        /*component*/
        n[0]
      )
    },
    {
      style: (
        /*$mergedProps*/
        n[1].elem_style
      )
    },
    {
      className: U(
        /*$mergedProps*/
        n[1].elem_classes
      )
    },
    {
      id: (
        /*$mergedProps*/
        n[1].elem_id
      )
    },
    /*$mergedProps*/
    n[1].props,
    R(
      /*$mergedProps*/
      n[1]
    ),
    {
      slots: (
        /*$slots*/
        n[2]
      )
    }
  ];
  let l = {
    $$slots: {
      default: [Ae]
    },
    $$scope: {
      ctx: n
    }
  };
  for (let s = 0; s < t.length; s += 1)
    l = pe(l, t[s]);
  return e = new /*TypographyBase*/
  n[20]({
    props: l
  }), {
    c() {
      be(e.$$.fragment);
    },
    m(s, i) {
      Se(e, s, i), o = !0;
    },
    p(s, i) {
      const c = i & /*component, $mergedProps, $slots*/
      7 ? ke(t, [i & /*component*/
      1 && {
        component: (
          /*component*/
          s[0]
        )
      }, i & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, i & /*$mergedProps*/
      2 && {
        className: U(
          /*$mergedProps*/
          s[1].elem_classes
        )
      }, i & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, i & /*$mergedProps*/
      2 && X(
        /*$mergedProps*/
        s[1].props
      ), i & /*$mergedProps*/
      2 && X(R(
        /*$mergedProps*/
        s[1]
      )), i & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }]) : {};
      i & /*$$scope, $mergedProps*/
      262146 && (c.$$scope = {
        dirty: i,
        ctx: s
      }), e.$set(c);
    },
    i(s) {
      o || (v(e.$$.fragment, s), o = !0);
    },
    o(s) {
      k(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ge(e, s);
    }
  };
}
function ze(n) {
  let e = (
    /*$mergedProps*/
    n[1].value + ""
  ), o;
  return {
    c() {
      o = je(e);
    },
    m(t, l) {
      E(t, o, l);
    },
    p(t, l) {
      l & /*$mergedProps*/
      2 && e !== (e = /*$mergedProps*/
      t[1].value + "") && Pe(o, e);
    },
    i: p,
    o: p,
    d(t) {
      t && $(o);
    }
  };
}
function Ie(n) {
  let e;
  const o = (
    /*#slots*/
    n[17].default
  ), t = he(
    o,
    n,
    /*$$scope*/
    n[18],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(l, s) {
      t && t.m(l, s), e = !0;
    },
    p(l, s) {
      t && t.p && (!e || s & /*$$scope*/
      262144) && $e(
        t,
        o,
        l,
        /*$$scope*/
        l[18],
        e ? ve(
          o,
          /*$$scope*/
          l[18],
          s,
          null
        ) : ye(
          /*$$scope*/
          l[18]
        ),
        null
      );
    },
    i(l) {
      e || (v(t, l), e = !0);
    },
    o(l) {
      k(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Ae(n) {
  let e, o, t, l;
  const s = [Ie, ze], i = [];
  function c(r, u) {
    return (
      /*$mergedProps*/
      r[1]._internal.layout ? 0 : 1
    );
  }
  return e = c(n), o = i[e] = s[e](n), {
    c() {
      o.c(), t = O();
    },
    m(r, u) {
      i[e].m(r, u), E(r, t, u), l = !0;
    },
    p(r, u) {
      let f = e;
      e = c(r), e === f ? i[e].p(r, u) : (Z(), k(i[f], 1, 1, () => {
        i[f] = null;
      }), V(), o = i[e], o ? o.p(r, u) : (o = i[e] = s[e](r), o.c()), v(o, 1), o.m(t.parentNode, t));
    },
    i(r) {
      l || (v(o), l = !0);
    },
    o(r) {
      k(o), l = !1;
    },
    d(r) {
      r && $(t), i[e].d(r);
    }
  };
}
function Oe(n) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function Be(n) {
  let e, o, t = (
    /*$mergedProps*/
    n[1].visible && Y(n)
  );
  return {
    c() {
      t && t.c(), e = O();
    },
    m(l, s) {
      t && t.m(l, s), E(l, e, s), o = !0;
    },
    p(l, [s]) {
      /*$mergedProps*/
      l[1].visible ? t ? (t.p(l, s), s & /*$mergedProps*/
      2 && v(t, 1)) : (t = Y(l), t.c(), v(t, 1), t.m(e.parentNode, e)) : t && (Z(), k(t, 1, 1, () => {
        t = null;
      }), V());
    },
    i(l) {
      o || (v(t), o = !0);
    },
    o(l) {
      k(t), o = !1;
    },
    d(l) {
      l && $(e), t && t.d(l);
    }
  };
}
function xe(n, e, o) {
  let t, l, s, {
    $$slots: i = {},
    $$scope: c
  } = e;
  const r = W(() => import("./typography.base-DylI2j_M.js"));
  let {
    component: u
  } = e, {
    gradio: f = {}
  } = e, {
    props: m = {}
  } = e;
  const b = y(m);
  q(n, b, (a) => o(16, t = a));
  let {
    _internal: _ = {}
  } = e, {
    value: d = ""
  } = e, {
    as_item: g = void 0
  } = e, {
    visible: w = !0
  } = e, {
    elem_id: P = ""
  } = e, {
    elem_classes: j = []
  } = e, {
    elem_style: N = {}
  } = e;
  const [B, J] = ce({
    gradio: f,
    props: t,
    _internal: _,
    value: d,
    visible: w,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: g
  });
  q(n, B, (a) => o(1, l = a));
  const x = ie();
  return q(n, x, (a) => o(2, s = a)), n.$$set = (a) => {
    "component" in a && o(0, u = a.component), "gradio" in a && o(7, f = a.gradio), "props" in a && o(8, m = a.props), "_internal" in a && o(9, _ = a._internal), "value" in a && o(10, d = a.value), "as_item" in a && o(11, g = a.as_item), "visible" in a && o(12, w = a.visible), "elem_id" in a && o(13, P = a.elem_id), "elem_classes" in a && o(14, j = a.elem_classes), "elem_style" in a && o(15, N = a.elem_style), "$$scope" in a && o(18, c = a.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    256 && b.update((a) => ({
      ...a,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, value, visible, elem_id, elem_classes, elem_style, as_item*/
    130688 && J({
      gradio: f,
      props: t,
      _internal: _,
      value: d,
      visible: w,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: g
    });
  }, [u, l, s, r, b, B, x, f, m, _, d, g, w, P, j, N, t, i, c];
}
class Re extends de {
  constructor(e) {
    super(), Ce(this, e, xe, Be, Ke, {
      component: 0,
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get component() {
    return this.$$.ctx[0];
  }
  set component(e) {
    this.$$set({
      component: e
    }), h();
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), h();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), h();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), h();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(e) {
    this.$$set({
      value: e
    }), h();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), h();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), h();
  }
}
const {
  SvelteComponent: Ue,
  assign: z,
  create_component: Xe,
  create_slot: Ye,
  destroy_component: De,
  exclude_internal_props: D,
  flush: Fe,
  get_all_dirty_from_scope: Le,
  get_slot_changes: Me,
  get_spread_object: Te,
  get_spread_update: Ve,
  init: Ze,
  mount_component: Ge,
  safe_not_equal: He,
  transition_in: G,
  transition_out: H,
  update_slot_base: Je
} = window.__gradio__svelte__internal;
function Qe(n) {
  let e;
  const o = (
    /*#slots*/
    n[2].default
  ), t = Ye(
    o,
    n,
    /*$$scope*/
    n[3],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(l, s) {
      t && t.m(l, s), e = !0;
    },
    p(l, s) {
      t && t.p && (!e || s & /*$$scope*/
      8) && Je(
        t,
        o,
        l,
        /*$$scope*/
        l[3],
        e ? Me(
          o,
          /*$$scope*/
          l[3],
          s,
          null
        ) : Le(
          /*$$scope*/
          l[3]
        ),
        null
      );
    },
    i(l) {
      e || (G(t, l), e = !0);
    },
    o(l) {
      H(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function We(n) {
  let e, o;
  const t = [
    /*$$props*/
    n[1],
    {
      value: (
        /*value*/
        n[0]
      )
    },
    {
      component: "title"
    }
  ];
  let l = {
    $$slots: {
      default: [Qe]
    },
    $$scope: {
      ctx: n
    }
  };
  for (let s = 0; s < t.length; s += 1)
    l = z(l, t[s]);
  return e = new Re({
    props: l
  }), {
    c() {
      Xe(e.$$.fragment);
    },
    m(s, i) {
      Ge(e, s, i), o = !0;
    },
    p(s, [i]) {
      const c = i & /*$$props, value*/
      3 ? Ve(t, [i & /*$$props*/
      2 && Te(
        /*$$props*/
        s[1]
      ), i & /*value*/
      1 && {
        value: (
          /*value*/
          s[0]
        )
      }, t[2]]) : {};
      i & /*$$scope*/
      8 && (c.$$scope = {
        dirty: i,
        ctx: s
      }), e.$set(c);
    },
    i(s) {
      o || (G(e.$$.fragment, s), o = !0);
    },
    o(s) {
      H(e.$$.fragment, s), o = !1;
    },
    d(s) {
      De(e, s);
    }
  };
}
function et(n, e, o) {
  let {
    $$slots: t = {},
    $$scope: l
  } = e, {
    value: s = ""
  } = e;
  return n.$$set = (i) => {
    o(1, e = z(z({}, e), D(i))), "value" in i && o(0, s = i.value), "$$scope" in i && o(3, l = i.$$scope);
  }, e = D(e), [s, e, t, l];
}
class st extends Ue {
  constructor(e) {
    super(), Ze(this, e, et, We, He, {
      value: 0
    });
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), Fe();
  }
}
export {
  st as I,
  C as a,
  U as c,
  tt as d,
  nt as g,
  y as w
};
