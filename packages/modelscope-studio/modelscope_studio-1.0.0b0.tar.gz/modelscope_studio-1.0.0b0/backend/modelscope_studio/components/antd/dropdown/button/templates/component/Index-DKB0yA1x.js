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
function V(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], r = u.split("_"), c = (...m) => {
        const p = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return e.dispatch(u.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let m = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = m;
        for (let f = 1; f < r.length - 1; f++) {
          const d = {
            ...n.props[r[f]] || {}
          };
          m[r[f]] = d, m = d;
        }
        const p = r[r.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = c, i;
      }
      const _ = r[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = c;
    }
    return i;
  }, {});
}
function K() {
}
function T(t) {
  return t();
}
function W(t) {
  t.forEach(T);
}
function $(t) {
  return typeof t == "function";
}
function ee(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function U(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return K;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function C(t) {
  let e;
  return U(t, (o) => e = o)(), e;
}
const S = [];
function te(t, e) {
  return {
    subscribe: g(t, e).subscribe
  };
}
function g(t, e = K) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(u) {
    if (ee(t, u) && (t = u, o)) {
      const r = !S.length;
      for (const c of n)
        c[1](), S.push(c, t);
      if (r) {
        for (let c = 0; c < S.length; c += 2)
          S[c][0](S[c + 1]);
        S.length = 0;
      }
    }
  }
  function s(u) {
    i(u(t));
  }
  function l(u, r = K) {
    const c = [u, r];
    return n.add(c), n.size === 1 && (o = e(i, s) || K), u(t), () => {
      n.delete(c), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
function Be(t, e, o) {
  const n = !Array.isArray(t), i = n ? [t] : t;
  if (!i.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const s = e.length < 2;
  return te(o, (l, u) => {
    let r = !1;
    const c = [];
    let _ = 0, m = K;
    const p = () => {
      if (_)
        return;
      m();
      const d = e(n ? c[0] : c, l, u);
      s ? l(d) : m = $(d) ? d : K;
    }, f = i.map((d, y) => U(d, (v) => {
      c[y] = v, _ &= ~(1 << y), r && p();
    }, () => {
      _ |= 1 << y;
    }));
    return r = !0, p(), function() {
      W(f), m(), r = !1;
    };
  });
}
const {
  getContext: z,
  setContext: A
} = window.__gradio__svelte__internal, ne = "$$ms-gr-antd-slots-key";
function se() {
  const t = g({});
  return A(ne, t);
}
const oe = "$$ms-gr-antd-context-key";
function ie(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = re(), o = ue({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), le();
  const n = z(oe), i = ((u = C(n)) == null ? void 0 : u.as_item) || t.as_item, s = n ? i ? C(n)[i] : C(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: c
    } = C(l);
    c && (r = r[c]), l.update((_) => ({
      ..._,
      ...r
    }));
  }), [l, (r) => {
    const c = r.as_item ? C(n)[r.as_item] : C(n);
    return l.set({
      ...r,
      ...c
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function le() {
  A(X, g(void 0));
}
function re() {
  return z(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function ue({
  slot: t,
  index: e,
  subIndex: o
}) {
  return A(Y, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function De() {
  return z(Y);
}
function ce(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var L = {
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
        var u = arguments[l];
        u && (s = i(s, n(u)));
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
      for (var u in s)
        e.call(s, u) && s[u] && (l = i(l, u));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(L);
var ae = L.exports;
const B = /* @__PURE__ */ ce(ae), {
  getContext: fe,
  setContext: _e
} = window.__gradio__svelte__internal;
function me(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function o(i = ["default"]) {
    const s = i.reduce((l, u) => (l[u] = g([]), l), {});
    return _e(e, {
      itemsMap: s,
      allowedSlots: i
    }), s;
  }
  function n() {
    const {
      itemsMap: i,
      allowedSlots: s
    } = fe(e);
    return function(l, u, r) {
      i && (l ? i[l].update((c) => {
        const _ = [...c];
        return s.includes(l) ? _[u] = r : _[u] = void 0, _;
      }) : s.includes("default") && i.default.update((c) => {
        const _ = [...c];
        return _[u] = r, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: de,
  getSetItemFn: Re
} = me("menu"), {
  SvelteComponent: be,
  assign: pe,
  check_outros: Z,
  component_subscribe: N,
  create_component: he,
  create_slot: ge,
  destroy_component: ye,
  detach: j,
  empty: O,
  flush: h,
  get_all_dirty_from_scope: we,
  get_slot_changes: ke,
  get_spread_object: D,
  get_spread_update: ve,
  group_outros: G,
  handle_promise: Ce,
  init: Se,
  insert: E,
  mount_component: Ke,
  noop: b,
  safe_not_equal: Ie,
  set_data: xe,
  text: Pe,
  transition_in: w,
  transition_out: k,
  update_await_block_branch: Ne,
  update_slot_base: je
} = window.__gradio__svelte__internal;
function R(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Fe,
    then: ze,
    catch: Ee,
    value: 21,
    blocks: [, , ,]
  };
  return Ce(
    /*AwaitedDropdownButton*/
    t[3],
    n
  ), {
    c() {
      e = O(), n.block.c();
    },
    m(i, s) {
      E(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, Ne(n, t, s);
    },
    i(i) {
      o || (w(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        k(l);
      }
      o = !1;
    },
    d(i) {
      i && j(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function Ee(t) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function ze(t) {
  let e, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: B(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-dropdown-button"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    /*$mergedProps*/
    t[0].props,
    V(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    },
    {
      menuItems: (
        /*$items*/
        t[2]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [qe]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = pe(i, n[s]);
  return e = new /*DropdownButton*/
  t[21]({
    props: i
  }), {
    c() {
      he(e.$$.fragment);
    },
    m(s, l) {
      Ke(e, s, l), o = !0;
    },
    p(s, l) {
      const u = l & /*$mergedProps, $slots, $items*/
      7 ? ve(n, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: B(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-dropdown-button"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && D(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && D(V(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }, l & /*$items*/
      4 && {
        menuItems: (
          /*$items*/
          s[2]
        )
      }]) : {};
      l & /*$$scope, $mergedProps*/
      524289 && (u.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(u);
    },
    i(s) {
      o || (w(e.$$.fragment, s), o = !0);
    },
    o(s) {
      k(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ye(e, s);
    }
  };
}
function Ae(t) {
  let e = (
    /*$mergedProps*/
    t[0].value + ""
  ), o;
  return {
    c() {
      o = Pe(e);
    },
    m(n, i) {
      E(n, o, i);
    },
    p(n, i) {
      i & /*$mergedProps*/
      1 && e !== (e = /*$mergedProps*/
      n[0].value + "") && xe(o, e);
    },
    i: b,
    o: b,
    d(n) {
      n && j(o);
    }
  };
}
function Oe(t) {
  let e;
  const o = (
    /*#slots*/
    t[18].default
  ), n = ge(
    o,
    t,
    /*$$scope*/
    t[19],
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
      524288) && je(
        n,
        o,
        i,
        /*$$scope*/
        i[19],
        e ? ke(
          o,
          /*$$scope*/
          i[19],
          s,
          null
        ) : we(
          /*$$scope*/
          i[19]
        ),
        null
      );
    },
    i(i) {
      e || (w(n, i), e = !0);
    },
    o(i) {
      k(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function qe(t) {
  let e, o, n, i;
  const s = [Oe, Ae], l = [];
  function u(r, c) {
    return (
      /*$mergedProps*/
      r[0]._internal.layout ? 0 : 1
    );
  }
  return e = u(t), o = l[e] = s[e](t), {
    c() {
      o.c(), n = O();
    },
    m(r, c) {
      l[e].m(r, c), E(r, n, c), i = !0;
    },
    p(r, c) {
      let _ = e;
      e = u(r), e === _ ? l[e].p(r, c) : (G(), k(l[_], 1, 1, () => {
        l[_] = null;
      }), Z(), o = l[e], o ? o.p(r, c) : (o = l[e] = s[e](r), o.c()), w(o, 1), o.m(n.parentNode, n));
    },
    i(r) {
      i || (w(o), i = !0);
    },
    o(r) {
      k(o), i = !1;
    },
    d(r) {
      r && j(n), l[e].d(r);
    }
  };
}
function Fe(t) {
  return {
    c: b,
    m: b,
    p: b,
    i: b,
    o: b,
    d: b
  };
}
function Me(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && R(t)
  );
  return {
    c() {
      n && n.c(), e = O();
    },
    m(i, s) {
      n && n.m(i, s), E(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && w(n, 1)) : (n = R(i), n.c(), w(n, 1), n.m(e.parentNode, e)) : n && (G(), k(n, 1, 1, () => {
        n = null;
      }), Z());
    },
    i(i) {
      o || (w(n), o = !0);
    },
    o(i) {
      k(n), o = !1;
    },
    d(i) {
      i && j(e), n && n.d(i);
    }
  };
}
function Ve(t, e, o) {
  let n, i, s, l, {
    $$slots: u = {},
    $$scope: r
  } = e;
  const c = Q(() => import("./dropdown.button-B4U_KF1k.js"));
  let {
    gradio: _
  } = e, {
    props: m = {}
  } = e, {
    value: p = ""
  } = e;
  const f = g(m);
  N(t, f, (a) => o(17, n = a));
  let {
    _internal: d = {}
  } = e, {
    as_item: y
  } = e, {
    visible: v = !0
  } = e, {
    elem_id: I = ""
  } = e, {
    elem_classes: x = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [q, H] = ie({
    gradio: _,
    props: n,
    _internal: d,
    visible: v,
    elem_id: I,
    elem_classes: x,
    elem_style: P,
    as_item: y,
    value: p
  });
  N(t, q, (a) => o(0, i = a));
  const F = se();
  N(t, F, (a) => o(1, s = a));
  const {
    "menu.items": M
  } = de(["menu.items"]);
  return N(t, M, (a) => o(2, l = a)), t.$$set = (a) => {
    "gradio" in a && o(8, _ = a.gradio), "props" in a && o(9, m = a.props), "value" in a && o(10, p = a.value), "_internal" in a && o(11, d = a._internal), "as_item" in a && o(12, y = a.as_item), "visible" in a && o(13, v = a.visible), "elem_id" in a && o(14, I = a.elem_id), "elem_classes" in a && o(15, x = a.elem_classes), "elem_style" in a && o(16, P = a.elem_style), "$$scope" in a && o(19, r = a.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && f.update((a) => ({
      ...a,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    261376 && H({
      gradio: _,
      props: n,
      _internal: d,
      visible: v,
      elem_id: I,
      elem_classes: x,
      elem_style: P,
      as_item: y,
      value: p
    });
  }, [i, s, l, c, f, q, F, M, _, m, p, d, y, v, I, x, P, n, u, r];
}
class Ue extends be {
  constructor(e) {
    super(), Se(this, e, Ve, Me, Ie, {
      gradio: 8,
      props: 9,
      value: 10,
      _internal: 11,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), h();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(e) {
    this.$$set({
      props: e
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
  get _internal() {
    return this.$$.ctx[11];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), h();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), h();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), h();
  }
}
export {
  Ue as I,
  C as a,
  Be as d,
  De as g,
  g as w
};
