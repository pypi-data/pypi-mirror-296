async function J() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function Q(e) {
  return await J(), e().then((t) => t.default);
}
function M(e) {
  const {
    gradio: t,
    _internal: l,
    ...s
  } = e;
  return Object.keys(l).reduce((o, n) => {
    const i = n.match(/bind_(.+)_event/);
    if (i) {
      const c = i[1], u = c.split("_"), f = (...m) => {
        const p = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return t.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (u.length > 1) {
        let m = {
          ...s.props[u[0]] || {}
        };
        o[u[0]] = m;
        for (let a = 1; a < u.length - 1; a++) {
          const g = {
            ...s.props[u[a]] || {}
          };
          m[u[a]] = g, m = g;
        }
        const p = u[u.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, o;
      }
      const _ = u[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function z() {
}
function T(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function W(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return z;
  }
  const l = e.subscribe(...t);
  return l.unsubscribe ? () => l.unsubscribe() : l;
}
function y(e) {
  let t;
  return W(e, (l) => t = l)(), t;
}
const w = [];
function h(e, t = z) {
  let l;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (T(e, c) && (e = c, l)) {
      const u = !w.length;
      for (const f of s)
        f[1](), w.push(f, e);
      if (u) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(c) {
    o(c(e));
  }
  function i(c, u = z) {
    const f = [c, u];
    return s.add(f), s.size === 1 && (l = t(o, n) || z), c(e), () => {
      s.delete(f), s.size === 0 && l && (l(), l = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: i
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = h({});
  return O($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = oe(), l = le({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    l.slotKey.set(u);
  }), se();
  const s = E(te), o = ((c = y(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, i = h({
    ...e,
    ...n
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: f
    } = y(i);
    f && (u = u[f]), i.update((_) => ({
      ..._,
      ...u
    }));
  }), [i, (u) => {
    const f = u.as_item ? y(s)[u.as_item] : y(s);
    return i.set({
      ...u,
      ...f
    });
  }]) : [i, (u) => {
    i.set(u);
  }];
}
const Y = "$$ms-gr-antd-slot-key";
function se() {
  O(Y, h(void 0));
}
function oe() {
  return E(Y);
}
const x = "$$ms-gr-antd-component-slot-context-key";
function le({
  slot: e,
  index: t,
  subIndex: l
}) {
  return O(x, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(l)
  });
}
function Ve() {
  return E(x);
}
function ie(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var D = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function l() {
      for (var n = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (n = o(n, s(c)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return l.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var i = "";
      for (var c in n)
        t.call(n, c) && n[c] && (i = o(i, c));
      return i;
    }
    function o(n, i) {
      return i ? n ? n + " " + i : n + i : n;
    }
    e.exports ? (l.default = l, e.exports = l) : window.classNames = l;
  })();
})(D);
var re = D.exports;
const R = /* @__PURE__ */ ie(re), {
  getContext: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ae(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function l(o = ["default"]) {
    const n = o.reduce((i, c) => (i[c] = h([]), i), {});
    return ue(t, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = ce(t);
    return function(i, c, u) {
      o && (i ? o[i].update((f) => {
        const _ = [...f];
        return n.includes(i) ? _[c] = u : _[c] = void 0, _;
      }) : n.includes("default") && o.default.update((f) => {
        const _ = [...f];
        return _[c] = u, _;
      }));
    };
  }
  return {
    getItems: l,
    getSetItemFn: s
  };
}
const {
  getItems: fe,
  getSetItemFn: Ae
} = ae("collapse"), {
  SvelteComponent: _e,
  assign: me,
  check_outros: de,
  component_subscribe: v,
  create_component: pe,
  create_slot: be,
  destroy_component: he,
  detach: L,
  empty: Z,
  flush: b,
  get_all_dirty_from_scope: ge,
  get_slot_changes: ye,
  get_spread_object: U,
  get_spread_update: we,
  group_outros: Ce,
  handle_promise: ke,
  init: ve,
  insert: B,
  mount_component: Ke,
  noop: d,
  safe_not_equal: Se,
  transition_in: C,
  transition_out: K,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function X(e) {
  let t, l, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ee,
    then: Ne,
    catch: je,
    value: 24,
    blocks: [, , ,]
  };
  return ke(
    /*AwaitedCollapse*/
    e[5],
    s
  ), {
    c() {
      t = Z(), s.block.c();
    },
    m(o, n) {
      B(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, l = !0;
    },
    p(o, n) {
      e = o, Ie(s, e, n);
    },
    i(o) {
      l || (C(s.block), l = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const i = s.blocks[n];
        K(i);
      }
      l = !1;
    },
    d(o) {
      o && L(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function je(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Ne(e) {
  let t, l;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: R(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-collapse"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    /*$mergedProps*/
    e[1].props,
    M(
      /*$mergedProps*/
      e[1]
    ),
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      slotItems: (
        /*$items*/
        e[3].length > 0 ? (
          /*$items*/
          e[3]
        ) : (
          /*$children*/
          e[4]
        )
      )
    },
    {
      activeKey: (
        /*$mergedProps*/
        e[1].props.activeKey || /*$mergedProps*/
        e[1].value
      )
    },
    {
      onValueChange: (
        /*func*/
        e[21]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [ze]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = me(o, s[n]);
  return t = new /*Collapse*/
  e[24]({
    props: o
  }), {
    c() {
      pe(t.$$.fragment);
    },
    m(n, i) {
      Ke(t, n, i), l = !0;
    },
    p(n, i) {
      const c = i & /*$mergedProps, $slots, $items, $children, value*/
      31 ? we(s, [i & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, i & /*$mergedProps*/
      2 && {
        className: R(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-collapse"
        )
      }, i & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, i & /*$mergedProps*/
      2 && U(
        /*$mergedProps*/
        n[1].props
      ), i & /*$mergedProps*/
      2 && U(M(
        /*$mergedProps*/
        n[1]
      )), i & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, i & /*$items, $children*/
      24 && {
        slotItems: (
          /*$items*/
          n[3].length > 0 ? (
            /*$items*/
            n[3]
          ) : (
            /*$children*/
            n[4]
          )
        )
      }, i & /*$mergedProps*/
      2 && {
        activeKey: (
          /*$mergedProps*/
          n[1].props.activeKey || /*$mergedProps*/
          n[1].value
        )
      }, i & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[21]
        )
      }]) : {};
      i & /*$$scope*/
      4194304 && (c.$$scope = {
        dirty: i,
        ctx: n
      }), t.$set(c);
    },
    i(n) {
      l || (C(t.$$.fragment, n), l = !0);
    },
    o(n) {
      K(t.$$.fragment, n), l = !1;
    },
    d(n) {
      he(t, n);
    }
  };
}
function ze(e) {
  let t;
  const l = (
    /*#slots*/
    e[20].default
  ), s = be(
    l,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, n) {
      s && s.m(o, n), t = !0;
    },
    p(o, n) {
      s && s.p && (!t || n & /*$$scope*/
      4194304) && Pe(
        s,
        l,
        o,
        /*$$scope*/
        o[22],
        t ? ye(
          l,
          /*$$scope*/
          o[22],
          n,
          null
        ) : ge(
          /*$$scope*/
          o[22]
        ),
        null
      );
    },
    i(o) {
      t || (C(s, o), t = !0);
    },
    o(o) {
      K(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ee(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Oe(e) {
  let t, l, s = (
    /*$mergedProps*/
    e[1].visible && X(e)
  );
  return {
    c() {
      s && s.c(), t = Z();
    },
    m(o, n) {
      s && s.m(o, n), B(o, t, n), l = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && C(s, 1)) : (s = X(o), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (Ce(), K(s, 1, 1, () => {
        s = null;
      }), de());
    },
    i(o) {
      l || (C(s), l = !0);
    },
    o(o) {
      K(s), l = !1;
    },
    d(o) {
      o && L(t), s && s.d(o);
    }
  };
}
function qe(e, t, l) {
  let s, o, n, i, c, {
    $$slots: u = {},
    $$scope: f
  } = t;
  const _ = Q(() => import("./collapse-D5VXdV7M.js"));
  let {
    gradio: m
  } = t, {
    props: p = {}
  } = t;
  const a = h(p);
  v(e, a, (r) => l(19, s = r));
  let {
    _internal: g = {}
  } = t, {
    value: k
  } = t, {
    as_item: S
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: P = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: N = {}
  } = t;
  const [q, G] = ne({
    gradio: m,
    props: s,
    _internal: g,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: S,
    value: k
  });
  v(e, q, (r) => l(1, o = r));
  const V = ee();
  v(e, V, (r) => l(2, n = r));
  const {
    items: A,
    default: F
  } = fe(["default", "items"]);
  v(e, A, (r) => l(3, i = r)), v(e, F, (r) => l(4, c = r));
  const H = (r) => {
    l(0, k = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && l(11, m = r.gradio), "props" in r && l(12, p = r.props), "_internal" in r && l(13, g = r._internal), "value" in r && l(0, k = r.value), "as_item" in r && l(14, S = r.as_item), "visible" in r && l(15, I = r.visible), "elem_id" in r && l(16, P = r.elem_id), "elem_classes" in r && l(17, j = r.elem_classes), "elem_style" in r && l(18, N = r.elem_style), "$$scope" in r && l(22, f = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && a.update((r) => ({
      ...r,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    1042433 && G({
      gradio: m,
      props: s,
      _internal: g,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: S,
      value: k
    });
  }, [k, o, n, i, c, _, a, q, V, A, F, m, p, g, S, I, P, j, N, s, u, H, f];
}
class Fe extends _e {
  constructor(t) {
    super(), ve(this, t, qe, Oe, Se, {
      gradio: 11,
      props: 12,
      _internal: 13,
      value: 0,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[11];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  Fe as I,
  Ve as g,
  h as w
};
