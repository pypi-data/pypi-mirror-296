async function Q() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function T(t) {
  return await Q(), t().then((e) => e.default);
}
function X(t) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = t;
  return Object.keys(i).reduce((l, n) => {
    const o = n.match(/bind_(.+)_event/);
    if (o) {
      const a = o[1], c = a.split("_"), f = (...d) => {
        const b = d.map((u) => d && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
        return e.dispatch(a.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let d = {
          ...s.props[c[0]] || {}
        };
        l[c[0]] = d;
        for (let u = 1; u < c.length - 1; u++) {
          const h = {
            ...s.props[c[u]] || {}
          };
          d[c[u]] = h, d = h;
        }
        const b = c[c.length - 1];
        return d[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, l;
      }
      const g = c[0];
      l[`on${g.slice(0, 1).toUpperCase()}${g.slice(1)}`] = f;
    }
    return l;
  }, {});
}
function O() {
}
function W(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function $(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return O;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return $(t, (i) => e = i)(), e;
}
const w = [];
function p(t, e = O) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function l(a) {
    if (W(t, a) && (t = a, i)) {
      const c = !w.length;
      for (const f of s)
        f[1](), w.push(f, t);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(a) {
    l(a(t));
  }
  function o(a, c = O) {
    const f = [a, c];
    return s.add(f), s.size === 1 && (i = e(l, n) || O), a(t), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: l,
    update: n,
    subscribe: o
  };
}
const {
  getContext: A,
  setContext: F
} = window.__gradio__svelte__internal, ee = "$$ms-gr-antd-slots-key";
function te() {
  const t = p({});
  return F(ee, t);
}
const ne = "$$ms-gr-antd-context-key";
function se(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = le(), i = oe({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), ie();
  const s = A(ne), l = ((a = y(s)) == null ? void 0 : a.as_item) || t.as_item, n = s ? l ? y(s)[l] : y(s) : {}, o = p({
    ...t,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: f
    } = y(o);
    f && (c = c[f]), o.update((g) => ({
      ...g,
      ...c
    }));
  }), [o, (c) => {
    const f = c.as_item ? y(s)[c.as_item] : y(s);
    return o.set({
      ...c,
      ...f
    });
  }]) : [o, (c) => {
    o.set(c);
  }];
}
const M = "$$ms-gr-antd-slot-key";
function ie() {
  F(M, p(void 0));
}
function le() {
  return A(M);
}
const V = "$$ms-gr-antd-component-slot-context-key";
function oe({
  slot: t,
  index: e,
  subIndex: i
}) {
  return F(V, {
    slotKey: p(t),
    slotIndex: p(e),
    subSlotIndex: p(i)
  });
}
function Ie() {
  return A(V);
}
function re(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var Z = {
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
    function i() {
      for (var n = "", o = 0; o < arguments.length; o++) {
        var a = arguments[o];
        a && (n = l(n, s(a)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var o = "";
      for (var a in n)
        e.call(n, a) && n[a] && (o = l(o, a));
      return o;
    }
    function l(n, o) {
      return o ? n ? n + " " + o : n + o : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(Z);
var ce = Z.exports;
const Y = /* @__PURE__ */ re(ce), {
  SvelteComponent: ue,
  assign: ae,
  check_outros: fe,
  component_subscribe: q,
  create_component: _e,
  create_slot: me,
  destroy_component: de,
  detach: B,
  empty: G,
  flush: _,
  get_all_dirty_from_scope: ge,
  get_slot_changes: be,
  get_spread_object: D,
  get_spread_update: he,
  group_outros: pe,
  handle_promise: ye,
  init: we,
  insert: H,
  mount_component: ke,
  noop: m,
  safe_not_equal: je,
  transition_in: k,
  transition_out: j,
  update_await_block_branch: xe,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function L(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Pe,
    then: Se,
    catch: Ke,
    value: 25,
    blocks: [, , ,]
  };
  return ye(
    /*AwaitedFlex*/
    t[2],
    s
  ), {
    c() {
      e = G(), s.block.c();
    },
    m(l, n) {
      H(l, e, n), s.block.m(l, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, i = !0;
    },
    p(l, n) {
      t = l, xe(s, t, n);
    },
    i(l) {
      i || (k(s.block), i = !0);
    },
    o(l) {
      for (let n = 0; n < 3; n += 1) {
        const o = s.blocks[n];
        j(o);
      }
      i = !1;
    },
    d(l) {
      l && B(e), s.block.d(l), s.token = null, s = null;
    }
  };
}
function Ke(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Se(t) {
  let e, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: Y(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-flex"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    {
      vertical: (
        /*$mergedProps*/
        t[0].vertical
      )
    },
    {
      wrap: (
        /*$mergedProps*/
        t[0].wrap
      )
    },
    {
      justify: (
        /*$mergedProps*/
        t[0].justify
      )
    },
    {
      align: (
        /*$mergedProps*/
        t[0].align
      )
    },
    {
      flex: (
        /*$mergedProps*/
        t[0].flex
      )
    },
    {
      gap: (
        /*$mergedProps*/
        t[0].gap
      )
    },
    {
      component: (
        /*$mergedProps*/
        t[0].component
      )
    },
    /*$mergedProps*/
    t[0].props,
    X(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    }
  ];
  let l = {
    $$slots: {
      default: [ve]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    l = ae(l, s[n]);
  return e = new /*Flex*/
  t[25]({
    props: l
  }), {
    c() {
      _e(e.$$.fragment);
    },
    m(n, o) {
      ke(e, n, o), i = !0;
    },
    p(n, o) {
      const a = o & /*$mergedProps, $slots*/
      3 ? he(s, [o & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, o & /*$mergedProps*/
      1 && {
        className: Y(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-flex"
        )
      }, o & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, o & /*$mergedProps*/
      1 && {
        vertical: (
          /*$mergedProps*/
          n[0].vertical
        )
      }, o & /*$mergedProps*/
      1 && {
        wrap: (
          /*$mergedProps*/
          n[0].wrap
        )
      }, o & /*$mergedProps*/
      1 && {
        justify: (
          /*$mergedProps*/
          n[0].justify
        )
      }, o & /*$mergedProps*/
      1 && {
        align: (
          /*$mergedProps*/
          n[0].align
        )
      }, o & /*$mergedProps*/
      1 && {
        flex: (
          /*$mergedProps*/
          n[0].flex
        )
      }, o & /*$mergedProps*/
      1 && {
        gap: (
          /*$mergedProps*/
          n[0].gap
        )
      }, o & /*$mergedProps*/
      1 && {
        component: (
          /*$mergedProps*/
          n[0].component
        )
      }, o & /*$mergedProps*/
      1 && D(
        /*$mergedProps*/
        n[0].props
      ), o & /*$mergedProps*/
      1 && D(X(
        /*$mergedProps*/
        n[0]
      )), o & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }]) : {};
      o & /*$$scope*/
      8388608 && (a.$$scope = {
        dirty: o,
        ctx: n
      }), e.$set(a);
    },
    i(n) {
      i || (k(e.$$.fragment, n), i = !0);
    },
    o(n) {
      j(e.$$.fragment, n), i = !1;
    },
    d(n) {
      de(e, n);
    }
  };
}
function ve(t) {
  let e;
  const i = (
    /*#slots*/
    t[22].default
  ), s = me(
    i,
    t,
    /*$$scope*/
    t[23],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(l, n) {
      s && s.m(l, n), e = !0;
    },
    p(l, n) {
      s && s.p && (!e || n & /*$$scope*/
      8388608) && Ce(
        s,
        i,
        l,
        /*$$scope*/
        l[23],
        e ? be(
          i,
          /*$$scope*/
          l[23],
          n,
          null
        ) : ge(
          /*$$scope*/
          l[23]
        ),
        null
      );
    },
    i(l) {
      e || (k(s, l), e = !0);
    },
    o(l) {
      j(s, l), e = !1;
    },
    d(l) {
      s && s.d(l);
    }
  };
}
function Pe(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ne(t) {
  let e, i, s = (
    /*$mergedProps*/
    t[0].visible && L(t)
  );
  return {
    c() {
      s && s.c(), e = G();
    },
    m(l, n) {
      s && s.m(l, n), H(l, e, n), i = !0;
    },
    p(l, [n]) {
      /*$mergedProps*/
      l[0].visible ? s ? (s.p(l, n), n & /*$mergedProps*/
      1 && k(s, 1)) : (s = L(l), s.c(), k(s, 1), s.m(e.parentNode, e)) : s && (pe(), j(s, 1, 1, () => {
        s = null;
      }), fe());
    },
    i(l) {
      i || (k(s), i = !0);
    },
    o(l) {
      j(s), i = !1;
    },
    d(l) {
      l && B(e), s && s.d(l);
    }
  };
}
function ze(t, e, i) {
  let s, l, n, {
    $$slots: o = {},
    $$scope: a
  } = e;
  const c = T(() => import("./flex-DHQVZXDK.js"));
  let {
    gradio: f
  } = e, {
    props: g = {}
  } = e;
  const d = p(g);
  q(t, d, (r) => i(21, s = r));
  let {
    _internal: b = {}
  } = e, {
    vertical: u
  } = e, {
    wrap: h
  } = e, {
    justify: x
  } = e, {
    align: C
  } = e, {
    flex: K
  } = e, {
    gap: S
  } = e, {
    component: v
  } = e, {
    as_item: P
  } = e, {
    visible: N = !0
  } = e, {
    elem_id: z = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: E = {}
  } = e;
  const [R, J] = se({
    gradio: f,
    props: s,
    _internal: b,
    visible: N,
    elem_id: z,
    elem_classes: I,
    elem_style: E,
    as_item: P,
    vertical: u,
    wrap: h,
    justify: x,
    align: C,
    flex: K,
    gap: S,
    component: v
  });
  q(t, R, (r) => i(0, l = r));
  const U = te();
  return q(t, U, (r) => i(1, n = r)), t.$$set = (r) => {
    "gradio" in r && i(6, f = r.gradio), "props" in r && i(7, g = r.props), "_internal" in r && i(8, b = r._internal), "vertical" in r && i(9, u = r.vertical), "wrap" in r && i(10, h = r.wrap), "justify" in r && i(11, x = r.justify), "align" in r && i(12, C = r.align), "flex" in r && i(13, K = r.flex), "gap" in r && i(14, S = r.gap), "component" in r && i(15, v = r.component), "as_item" in r && i(16, P = r.as_item), "visible" in r && i(17, N = r.visible), "elem_id" in r && i(18, z = r.elem_id), "elem_classes" in r && i(19, I = r.elem_classes), "elem_style" in r && i(20, E = r.elem_style), "$$scope" in r && i(23, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && d.update((r) => ({
      ...r,
      ...g
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, vertical, wrap, justify, align, flex, gap, component*/
    4194112 && J({
      gradio: f,
      props: s,
      _internal: b,
      visible: N,
      elem_id: z,
      elem_classes: I,
      elem_style: E,
      as_item: P,
      vertical: u,
      wrap: h,
      justify: x,
      align: C,
      flex: K,
      gap: S,
      component: v
    });
  }, [l, n, c, d, R, U, f, g, b, u, h, x, C, K, S, v, P, N, z, I, E, s, o, a];
}
class Ee extends ue {
  constructor(e) {
    super(), we(this, e, ze, Ne, je, {
      gradio: 6,
      props: 7,
      _internal: 8,
      vertical: 9,
      wrap: 10,
      justify: 11,
      align: 12,
      flex: 13,
      gap: 14,
      component: 15,
      as_item: 16,
      visible: 17,
      elem_id: 18,
      elem_classes: 19,
      elem_style: 20
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
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), _();
  }
  get vertical() {
    return this.$$.ctx[9];
  }
  set vertical(e) {
    this.$$set({
      vertical: e
    }), _();
  }
  get wrap() {
    return this.$$.ctx[10];
  }
  set wrap(e) {
    this.$$set({
      wrap: e
    }), _();
  }
  get justify() {
    return this.$$.ctx[11];
  }
  set justify(e) {
    this.$$set({
      justify: e
    }), _();
  }
  get align() {
    return this.$$.ctx[12];
  }
  set align(e) {
    this.$$set({
      align: e
    }), _();
  }
  get flex() {
    return this.$$.ctx[13];
  }
  set flex(e) {
    this.$$set({
      flex: e
    }), _();
  }
  get gap() {
    return this.$$.ctx[14];
  }
  set gap(e) {
    this.$$set({
      gap: e
    }), _();
  }
  get component() {
    return this.$$.ctx[15];
  }
  set component(e) {
    this.$$set({
      component: e
    }), _();
  }
  get as_item() {
    return this.$$.ctx[16];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), _();
  }
  get visible() {
    return this.$$.ctx[17];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), _();
  }
  get elem_id() {
    return this.$$.ctx[18];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), _();
  }
  get elem_classes() {
    return this.$$.ctx[19];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), _();
  }
  get elem_style() {
    return this.$$.ctx[20];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), _();
  }
}
export {
  Ee as I,
  Ie as g,
  p as w
};
