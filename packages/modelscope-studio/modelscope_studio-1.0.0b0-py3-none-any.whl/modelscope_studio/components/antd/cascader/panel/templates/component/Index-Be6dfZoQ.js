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
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), f = (...m) => {
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
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let t;
  return W(e, (i) => t = i)(), t;
}
const w = [];
function h(e, t = z) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (T(e, c) && (e = c, i)) {
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
  function l(c, u = z) {
    const f = [c, u];
    return s.add(f), s.size === 1 && (i = t(o, n) || z), c(e), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
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
  const t = oe(), i = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    i.slotKey.set(u);
  }), se();
  const s = E(te), o = ((c = y(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...e,
    ...n
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: f
    } = y(l);
    f && (u = u[f]), l.update((_) => ({
      ..._,
      ...u
    }));
  }), [l, (u) => {
    const f = u.as_item ? y(s)[u.as_item] : y(s);
    return l.set({
      ...u,
      ...f
    });
  }]) : [l, (u) => {
    l.set(u);
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
function ie({
  slot: e,
  index: t,
  subIndex: i
}) {
  return O(x, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(i)
  });
}
function Ve() {
  return E(x);
}
function le(e) {
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
    function i() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
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
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var c in n)
        t.call(n, c) && n[c] && (l = o(l, c));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(D);
var re = D.exports;
const R = /* @__PURE__ */ le(re), {
  getContext: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ae(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((l, c) => (l[c] = h([]), l), {});
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
    return function(l, c, u) {
      o && (l ? o[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[c] = u : _[c] = void 0, _;
      }) : n.includes("default") && o.default.update((f) => {
        const _ = [...f];
        return _[c] = u, _;
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
} = ae("cascader"), {
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
  mount_component: Se,
  noop: d,
  safe_not_equal: Ke,
  transition_in: C,
  transition_out: S,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function X(e) {
  let t, i, s = {
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
    /*AwaitedCascaderPanel*/
    e[5],
    s
  ), {
    c() {
      t = Z(), s.block.c();
    },
    m(o, n) {
      B(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, n) {
      e = o, Ie(s, e, n);
    },
    i(o) {
      i || (C(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        S(l);
      }
      i = !1;
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
  let t, i;
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
        "ms-gr-antd-cascader-panel"
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
      optionItems: (
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
  for (let n = 0; n < s.length; n += 1)
    o = me(o, s[n]);
  return t = new /*CascaderPanel*/
  e[24]({
    props: o
  }), {
    c() {
      pe(t.$$.fragment);
    },
    m(n, l) {
      Se(t, n, l), i = !0;
    },
    p(n, l) {
      const c = l & /*$mergedProps, $slots, $options, $children, value*/
      31 ? we(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: R(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-cascader-panel"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && U(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && U(M(
        /*$mergedProps*/
        n[1]
      )), l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          n[1].props.value ?? /*$mergedProps*/
          n[1].value
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*$options, $children*/
      24 && {
        optionItems: (
          /*$options*/
          n[3].length > 0 ? (
            /*$options*/
            n[3]
          ) : (
            /*$children*/
            n[4]
          )
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[21]
        )
      }]) : {};
      l & /*$$scope*/
      4194304 && (c.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(c);
    },
    i(n) {
      i || (C(t.$$.fragment, n), i = !0);
    },
    o(n) {
      S(t.$$.fragment, n), i = !1;
    },
    d(n) {
      he(t, n);
    }
  };
}
function ze(e) {
  let t;
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
    m(o, n) {
      s && s.m(o, n), t = !0;
    },
    p(o, n) {
      s && s.p && (!t || n & /*$$scope*/
      4194304) && Pe(
        s,
        i,
        o,
        /*$$scope*/
        o[22],
        t ? ye(
          i,
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
      S(s, o), t = !1;
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
  let t, i, s = (
    /*$mergedProps*/
    e[1].visible && X(e)
  );
  return {
    c() {
      s && s.c(), t = Z();
    },
    m(o, n) {
      s && s.m(o, n), B(o, t, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && C(s, 1)) : (s = X(o), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (Ce(), S(s, 1, 1, () => {
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
      o && L(t), s && s.d(o);
    }
  };
}
function qe(e, t, i) {
  let s, o, n, l, c, {
    $$slots: u = {},
    $$scope: f
  } = t;
  const _ = Q(() => import("./cascader.panel-CVXpF0V2.js"));
  let {
    gradio: m
  } = t, {
    props: p = {}
  } = t;
  const a = h(p);
  v(e, a, (r) => i(19, s = r));
  let {
    _internal: g = {}
  } = t, {
    value: k
  } = t, {
    as_item: K
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
    as_item: K,
    value: k
  });
  v(e, q, (r) => i(1, o = r));
  const V = ee();
  v(e, V, (r) => i(2, n = r));
  const {
    default: A,
    options: F
  } = fe(["default", "options"]);
  v(e, A, (r) => i(4, c = r)), v(e, F, (r) => i(3, l = r));
  const H = (r) => {
    i(0, k = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && i(11, m = r.gradio), "props" in r && i(12, p = r.props), "_internal" in r && i(13, g = r._internal), "value" in r && i(0, k = r.value), "as_item" in r && i(14, K = r.as_item), "visible" in r && i(15, I = r.visible), "elem_id" in r && i(16, P = r.elem_id), "elem_classes" in r && i(17, j = r.elem_classes), "elem_style" in r && i(18, N = r.elem_style), "$$scope" in r && i(22, f = r.$$scope);
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
      as_item: K,
      value: k
    });
  }, [k, o, n, l, c, _, a, q, V, A, F, m, p, g, K, I, P, j, N, s, u, H, f];
}
class Fe extends _e {
  constructor(t) {
    super(), ve(this, t, qe, Oe, Ke, {
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
