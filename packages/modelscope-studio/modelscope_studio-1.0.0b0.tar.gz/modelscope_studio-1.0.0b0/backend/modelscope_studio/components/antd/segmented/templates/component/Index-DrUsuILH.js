async function Q() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function T(e) {
  return await Q(), e().then((n) => n.default);
}
function M(e) {
  const {
    gradio: n,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, t) => {
    const l = t.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
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
        return n.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        o[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const h = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = h, m = h;
        }
        const p = c[c.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, o;
      }
      const _ = c[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function z() {
}
function W(e, n) {
  return e != e ? n == n : e !== n || e && typeof e == "object" || typeof e == "function";
}
function x(e, ...n) {
  if (e == null) {
    for (const s of n)
      s(void 0);
    return z;
  }
  const i = e.subscribe(...n);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let n;
  return x(e, (i) => n = i)(), n;
}
const w = [];
function g(e, n = z) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (W(e, u) && (e = u, i)) {
      const c = !w.length;
      for (const f of s)
        f[1](), w.push(f, e);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function t(u) {
    o(u(e));
  }
  function l(u, c = z) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (i = n(o, t) || z), u(e), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: t,
    subscribe: l
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = g({});
  return O($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = oe(), i = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  n && n.subscribe((c) => {
    i.slotKey.set(c);
  }), se();
  const s = E(te), o = ((u = y(s)) == null ? void 0 : u.as_item) || e.as_item, t = s ? o ? y(s)[o] : y(s) : {}, l = g({
    ...e,
    ...t
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((_) => ({
      ..._,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(s)[c.as_item] : y(s);
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
  O(Y, g(void 0));
}
function oe() {
  return E(Y);
}
const D = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: e,
  index: n,
  subIndex: i
}) {
  return O(D, {
    slotKey: g(e),
    slotIndex: g(n),
    subSlotIndex: g(i)
  });
}
function Ve() {
  return E(D);
}
function le(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var L = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var n = {}.hasOwnProperty;
    function i() {
      for (var t = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (t = o(t, s(u)));
      }
      return t;
    }
    function s(t) {
      if (typeof t == "string" || typeof t == "number")
        return t;
      if (typeof t != "object")
        return "";
      if (Array.isArray(t))
        return i.apply(null, t);
      if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]"))
        return t.toString();
      var l = "";
      for (var u in t)
        n.call(t, u) && t[u] && (l = o(l, u));
      return l;
    }
    function o(t, l) {
      return l ? t ? t + " " + l : t + l : t;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(L);
var re = L.exports;
const R = /* @__PURE__ */ le(re), {
  getContext: ue,
  setContext: ce
} = window.__gradio__svelte__internal;
function ae(e) {
  const n = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const t = o.reduce((l, u) => (l[u] = g([]), l), {});
    return ce(n, {
      itemsMap: t,
      allowedSlots: o
    }), t;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: t
    } = ue(n);
    return function(l, u, c) {
      o && (l ? o[l].update((f) => {
        const _ = [...f];
        return t.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : t.includes("default") && o.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: s
  };
}
const {
  getItems: fe,
  getSetItemFn: Ae
} = ae("segmented"), {
  SvelteComponent: _e,
  assign: me,
  check_outros: de,
  component_subscribe: v,
  create_component: pe,
  create_slot: be,
  destroy_component: ge,
  detach: Z,
  empty: B,
  flush: b,
  get_all_dirty_from_scope: he,
  get_slot_changes: ye,
  get_spread_object: U,
  get_spread_update: we,
  group_outros: Ce,
  handle_promise: ke,
  init: ve,
  insert: G,
  mount_component: Se,
  noop: d,
  safe_not_equal: Ke,
  transition_in: C,
  transition_out: S,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function X(e) {
  let n, i, s = {
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
    /*AwaitedSegmented*/
    e[5],
    s
  ), {
    c() {
      n = B(), s.block.c();
    },
    m(o, t) {
      G(o, n, t), s.block.m(o, s.anchor = t), s.mount = () => n.parentNode, s.anchor = n, i = !0;
    },
    p(o, t) {
      e = o, Ie(s, e, t);
    },
    i(o) {
      i || (C(s.block), i = !0);
    },
    o(o) {
      for (let t = 0; t < 3; t += 1) {
        const l = s.blocks[t];
        S(l);
      }
      i = !1;
    },
    d(o) {
      o && Z(n), s.block.d(o), s.token = null, s = null;
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
  let n, i;
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
        "ms-gr-antd-segmented"
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
      value: (
        /*$mergedProps*/
        e[1].props.value ?? /*$mergedProps*/
        e[1].value
      )
    },
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      options: (
        /*$mergedProps*/
        e[1].props.options
      )
    },
    {
      slotItems: (
        /*$options*/
        e[3].length > 0 ? (
          /*$options*/
          e[3]
        ) : (
          /*$children*/
          e[4]
        )
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
  for (let t = 0; t < s.length; t += 1)
    o = me(o, s[t]);
  return n = new /*Segmented*/
  e[24]({
    props: o
  }), {
    c() {
      pe(n.$$.fragment);
    },
    m(t, l) {
      Se(n, t, l), i = !0;
    },
    p(t, l) {
      const u = l & /*$mergedProps, $slots, $options, $children, value*/
      31 ? we(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          t[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: R(
          /*$mergedProps*/
          t[1].elem_classes,
          "ms-gr-antd-segmented"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          t[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && U(
        /*$mergedProps*/
        t[1].props
      ), l & /*$mergedProps*/
      2 && U(M(
        /*$mergedProps*/
        t[1]
      )), l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          t[1].props.value ?? /*$mergedProps*/
          t[1].value
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          t[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        options: (
          /*$mergedProps*/
          t[1].props.options
        )
      }, l & /*$options, $children*/
      24 && {
        slotItems: (
          /*$options*/
          t[3].length > 0 ? (
            /*$options*/
            t[3]
          ) : (
            /*$children*/
            t[4]
          )
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          t[21]
        )
      }]) : {};
      l & /*$$scope*/
      4194304 && (u.$$scope = {
        dirty: l,
        ctx: t
      }), n.$set(u);
    },
    i(t) {
      i || (C(n.$$.fragment, t), i = !0);
    },
    o(t) {
      S(n.$$.fragment, t), i = !1;
    },
    d(t) {
      ge(n, t);
    }
  };
}
function ze(e) {
  let n;
  const i = (
    /*#slots*/
    e[20].default
  ), s = be(
    i,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, t) {
      s && s.m(o, t), n = !0;
    },
    p(o, t) {
      s && s.p && (!n || t & /*$$scope*/
      4194304) && Pe(
        s,
        i,
        o,
        /*$$scope*/
        o[22],
        n ? ye(
          i,
          /*$$scope*/
          o[22],
          t,
          null
        ) : he(
          /*$$scope*/
          o[22]
        ),
        null
      );
    },
    i(o) {
      n || (C(s, o), n = !0);
    },
    o(o) {
      S(s, o), n = !1;
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
  let n, i, s = (
    /*$mergedProps*/
    e[1].visible && X(e)
  );
  return {
    c() {
      s && s.c(), n = B();
    },
    m(o, t) {
      s && s.m(o, t), G(o, n, t), i = !0;
    },
    p(o, [t]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, t), t & /*$mergedProps*/
      2 && C(s, 1)) : (s = X(o), s.c(), C(s, 1), s.m(n.parentNode, n)) : s && (Ce(), S(s, 1, 1, () => {
        s = null;
      }), de());
    },
    i(o) {
      i || (C(s), i = !0);
    },
    o(o) {
      S(s), i = !1;
    },
    d(o) {
      o && Z(n), s && s.d(o);
    }
  };
}
function qe(e, n, i) {
  let s, o, t, l, u, {
    $$slots: c = {},
    $$scope: f
  } = n;
  const _ = T(() => import("./segmented-DeWJcavC.js"));
  let {
    gradio: m
  } = n, {
    props: p = {}
  } = n;
  const a = g(p);
  v(e, a, (r) => i(19, s = r));
  let {
    _internal: h = {}
  } = n, {
    value: k
  } = n, {
    as_item: K
  } = n, {
    visible: I = !0
  } = n, {
    elem_id: P = ""
  } = n, {
    elem_classes: j = []
  } = n, {
    elem_style: N = {}
  } = n;
  const [q, H] = ne({
    gradio: m,
    props: s,
    _internal: h,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: K,
    value: k
  });
  v(e, q, (r) => i(1, o = r));
  const V = ee();
  v(e, V, (r) => i(2, t = r));
  const {
    options: A,
    default: F
  } = fe(["options", "default"]);
  v(e, A, (r) => i(3, l = r)), v(e, F, (r) => i(4, u = r));
  const J = (r) => {
    i(0, k = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && i(11, m = r.gradio), "props" in r && i(12, p = r.props), "_internal" in r && i(13, h = r._internal), "value" in r && i(0, k = r.value), "as_item" in r && i(14, K = r.as_item), "visible" in r && i(15, I = r.visible), "elem_id" in r && i(16, P = r.elem_id), "elem_classes" in r && i(17, j = r.elem_classes), "elem_style" in r && i(18, N = r.elem_style), "$$scope" in r && i(22, f = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && a.update((r) => ({
      ...r,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    1042433 && H({
      gradio: m,
      props: s,
      _internal: h,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: K,
      value: k
    });
  }, [k, o, t, l, u, _, a, q, V, A, F, m, p, h, K, I, P, j, N, s, c, J, f];
}
class Fe extends _e {
  constructor(n) {
    super(), ve(this, n, qe, Oe, Ke, {
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
  set gradio(n) {
    this.$$set({
      gradio: n
    }), b();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(n) {
    this.$$set({
      props: n
    }), b();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(n) {
    this.$$set({
      _internal: n
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(n) {
    this.$$set({
      value: n
    }), b();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(n) {
    this.$$set({
      as_item: n
    }), b();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(n) {
    this.$$set({
      visible: n
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(n) {
    this.$$set({
      elem_id: n
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(n) {
    this.$$set({
      elem_classes: n
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(n) {
    this.$$set({
      elem_style: n
    }), b();
  }
}
export {
  Fe as I,
  Ve as g,
  g as w
};
