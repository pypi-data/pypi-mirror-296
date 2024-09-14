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
function R(t) {
  const {
    gradio: e,
    _internal: o,
    ...s
  } = t;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
        const b = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
          type: a.type,
          detail: a.detail,
          timestamp: a.timeStamp,
          clientX: a.clientX,
          clientY: a.clientY,
          targetId: a.target.id,
          targetClassName: a.target.className,
          altKey: a.altKey,
          ctrlKey: a.ctrlKey,
          shiftKey: a.shiftKey,
          metaKey: a.metaKey
        } : a);
        return e.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const p = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = p, m = p;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const _ = c[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function E() {
}
function T(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function W(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return E;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function w(t) {
  let e;
  return W(t, (o) => e = o)(), e;
}
const y = [];
function h(t, e = E) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(u) {
    if (T(t, u) && (t = u, o)) {
      const c = !y.length;
      for (const f of s)
        f[1](), y.push(f, t);
      if (c) {
        for (let f = 0; f < y.length; f += 2)
          y[f][0](y[f + 1]);
        y.length = 0;
      }
    }
  }
  function n(u) {
    i(u(t));
  }
  function l(u, c = E) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (o = e(i, n) || E), u(t), () => {
      s.delete(f), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: n,
    subscribe: l
  };
}
const {
  getContext: O,
  setContext: q
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const t = h({});
  return q($, t);
}
const te = "$$ms-gr-antd-context-key";
function ne(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ie(), o = oe({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    o.slotKey.set(c);
  }), se();
  const s = O(te), i = ((u = w(s)) == null ? void 0 : u.as_item) || t.as_item, n = s ? i ? w(s)[i] : w(s) : {}, l = h({
    ...t,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: f
    } = w(l);
    f && (c = c[f]), l.update((_) => ({
      ..._,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? w(s)[c.as_item] : w(s);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const Y = "$$ms-gr-antd-slot-key";
function se() {
  q(Y, h(void 0));
}
function ie() {
  return O(Y);
}
const D = "$$ms-gr-antd-component-slot-context-key";
function oe({
  slot: t,
  index: e,
  subIndex: o
}) {
  return q(D, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(o)
  });
}
function qe() {
  return O(D);
}
function le(t) {
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
      for (var n = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (n = i(n, s(u)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var u in n)
        e.call(n, u) && n[u] && (l = i(l, u));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(L);
var re = L.exports;
const V = /* @__PURE__ */ le(re), {
  getContext: ue,
  setContext: ce
} = window.__gradio__svelte__internal;
function ae(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function o(i = ["default"]) {
    const n = i.reduce((l, u) => (l[u] = h([]), l), {});
    return ce(e, {
      itemsMap: n,
      allowedSlots: i
    }), n;
  }
  function s() {
    const {
      itemsMap: i,
      allowedSlots: n
    } = ue(e);
    return function(l, u, c) {
      i && (l ? i[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : n.includes("default") && i.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: s
  };
}
const {
  getItems: fe,
  getSetItemFn: Ae
} = ae("grid"), {
  SvelteComponent: _e,
  assign: me,
  check_outros: de,
  component_subscribe: x,
  create_component: ge,
  create_slot: be,
  destroy_component: he,
  detach: Z,
  empty: B,
  flush: d,
  get_all_dirty_from_scope: pe,
  get_slot_changes: we,
  get_spread_object: U,
  get_spread_update: ye,
  group_outros: Ce,
  handle_promise: ke,
  init: Se,
  insert: G,
  mount_component: je,
  noop: g,
  safe_not_equal: Ke,
  transition_in: C,
  transition_out: k,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function X(t) {
  let e, o, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: xe,
    then: Ne,
    catch: ve,
    value: 24,
    blocks: [, , ,]
  };
  return ke(
    /*AwaitedRow*/
    t[3],
    s
  ), {
    c() {
      e = B(), s.block.c();
    },
    m(i, n) {
      G(i, e, n), s.block.m(i, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, o = !0;
    },
    p(i, n) {
      t = i, Ie(s, t, n);
    },
    i(i) {
      o || (C(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        k(l);
      }
      o = !1;
    },
    d(i) {
      i && Z(e), s.block.d(i), s.token = null, s = null;
    }
  };
}
function ve(t) {
  return {
    c: g,
    m: g,
    p: g,
    i: g,
    o: g,
    d: g
  };
}
function Ne(t) {
  let e, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: V(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-row"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    {
      align: (
        /*$mergedProps*/
        t[0].align
      )
    },
    {
      gutter: (
        /*$mergedProps*/
        t[0].gutter
      )
    },
    {
      justify: (
        /*$mergedProps*/
        t[0].justify
      )
    },
    {
      wrap: (
        /*$mergedProps*/
        t[0].wrap
      )
    },
    /*$mergedProps*/
    t[0].props,
    R(
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
      cols: (
        /*$cols*/
        t[2]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ze]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    i = me(i, s[n]);
  return e = new /*Row*/
  t[24]({
    props: i
  }), {
    c() {
      ge(e.$$.fragment);
    },
    m(n, l) {
      je(e, n, l), o = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, $cols*/
      7 ? ye(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: V(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-row"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && {
        align: (
          /*$mergedProps*/
          n[0].align
        )
      }, l & /*$mergedProps*/
      1 && {
        gutter: (
          /*$mergedProps*/
          n[0].gutter
        )
      }, l & /*$mergedProps*/
      1 && {
        justify: (
          /*$mergedProps*/
          n[0].justify
        )
      }, l & /*$mergedProps*/
      1 && {
        wrap: (
          /*$mergedProps*/
          n[0].wrap
        )
      }, l & /*$mergedProps*/
      1 && U(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && U(R(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$cols*/
      4 && {
        cols: (
          /*$cols*/
          n[2]
        )
      }]) : {};
      l & /*$$scope*/
      4194304 && (u.$$scope = {
        dirty: l,
        ctx: n
      }), e.$set(u);
    },
    i(n) {
      o || (C(e.$$.fragment, n), o = !0);
    },
    o(n) {
      k(e.$$.fragment, n), o = !1;
    },
    d(n) {
      he(e, n);
    }
  };
}
function ze(t) {
  let e;
  const o = (
    /*#slots*/
    t[21].default
  ), s = be(
    o,
    t,
    /*$$scope*/
    t[22],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(i, n) {
      s && s.m(i, n), e = !0;
    },
    p(i, n) {
      s && s.p && (!e || n & /*$$scope*/
      4194304) && Pe(
        s,
        o,
        i,
        /*$$scope*/
        i[22],
        e ? we(
          o,
          /*$$scope*/
          i[22],
          n,
          null
        ) : pe(
          /*$$scope*/
          i[22]
        ),
        null
      );
    },
    i(i) {
      e || (C(s, i), e = !0);
    },
    o(i) {
      k(s, i), e = !1;
    },
    d(i) {
      s && s.d(i);
    }
  };
}
function xe(t) {
  return {
    c: g,
    m: g,
    p: g,
    i: g,
    o: g,
    d: g
  };
}
function Ee(t) {
  let e, o, s = (
    /*$mergedProps*/
    t[0].visible && X(t)
  );
  return {
    c() {
      s && s.c(), e = B();
    },
    m(i, n) {
      s && s.m(i, n), G(i, e, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[0].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = X(i), s.c(), C(s, 1), s.m(e.parentNode, e)) : s && (Ce(), k(s, 1, 1, () => {
        s = null;
      }), de());
    },
    i(i) {
      o || (C(s), o = !0);
    },
    o(i) {
      k(s), o = !1;
    },
    d(i) {
      i && Z(e), s && s.d(i);
    }
  };
}
function Oe(t, e, o) {
  let s, i, n, l, {
    $$slots: u = {},
    $$scope: c
  } = e;
  const f = Q(() => import("./row-Cqcd2km1.js"));
  let {
    gradio: _
  } = e, {
    props: m = {}
  } = e;
  const b = h(m);
  x(t, b, (r) => o(20, s = r));
  let {
    _internal: a = {}
  } = e, {
    align: p
  } = e, {
    gutter: S
  } = e, {
    justify: j
  } = e, {
    wrap: K
  } = e, {
    as_item: I
  } = e, {
    visible: P = !0
  } = e, {
    elem_id: v = ""
  } = e, {
    elem_classes: N = []
  } = e, {
    elem_style: z = {}
  } = e;
  const [A, H] = ne({
    gradio: _,
    props: s,
    _internal: a,
    visible: P,
    elem_id: v,
    elem_classes: N,
    elem_style: z,
    as_item: I,
    align: p,
    gutter: S,
    justify: j,
    wrap: K
  });
  x(t, A, (r) => o(0, i = r));
  const F = ee();
  x(t, F, (r) => o(1, n = r));
  const {
    default: M
  } = fe();
  return x(t, M, (r) => o(2, l = r)), t.$$set = (r) => {
    "gradio" in r && o(8, _ = r.gradio), "props" in r && o(9, m = r.props), "_internal" in r && o(10, a = r._internal), "align" in r && o(11, p = r.align), "gutter" in r && o(12, S = r.gutter), "justify" in r && o(13, j = r.justify), "wrap" in r && o(14, K = r.wrap), "as_item" in r && o(15, I = r.as_item), "visible" in r && o(16, P = r.visible), "elem_id" in r && o(17, v = r.elem_id), "elem_classes" in r && o(18, N = r.elem_classes), "elem_style" in r && o(19, z = r.elem_style), "$$scope" in r && o(22, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && b.update((r) => ({
      ...r,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, align, gutter, justify, wrap*/
    2096384 && H({
      gradio: _,
      props: s,
      _internal: a,
      visible: P,
      elem_id: v,
      elem_classes: N,
      elem_style: z,
      as_item: I,
      align: p,
      gutter: S,
      justify: j,
      wrap: K
    });
  }, [i, n, l, f, b, A, F, M, _, m, a, p, S, j, K, I, P, v, N, z, s, u, c];
}
class Fe extends _e {
  constructor(e) {
    super(), Se(this, e, Oe, Ee, Ke, {
      gradio: 8,
      props: 9,
      _internal: 10,
      align: 11,
      gutter: 12,
      justify: 13,
      wrap: 14,
      as_item: 15,
      visible: 16,
      elem_id: 17,
      elem_classes: 18,
      elem_style: 19
    });
  }
  get gradio() {
    return this.$$.ctx[8];
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
  get align() {
    return this.$$.ctx[11];
  }
  set align(e) {
    this.$$set({
      align: e
    }), d();
  }
  get gutter() {
    return this.$$.ctx[12];
  }
  set gutter(e) {
    this.$$set({
      gutter: e
    }), d();
  }
  get justify() {
    return this.$$.ctx[13];
  }
  set justify(e) {
    this.$$set({
      justify: e
    }), d();
  }
  get wrap() {
    return this.$$.ctx[14];
  }
  set wrap(e) {
    this.$$set({
      wrap: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[15];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[17];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[18];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[19];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  Fe as I,
  qe as g,
  h as w
};
