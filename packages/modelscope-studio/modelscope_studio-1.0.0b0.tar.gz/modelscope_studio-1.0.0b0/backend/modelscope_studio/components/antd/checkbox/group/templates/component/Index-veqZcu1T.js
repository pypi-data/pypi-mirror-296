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
function F(e) {
  const {
    gradio: t,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
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
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
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
          const g = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = g, m = g;
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
function N() {
}
function T(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function W(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return N;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let t;
  return W(e, (i) => t = i)(), t;
}
const w = [];
function h(e, t = N) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (T(e, u) && (e = u, i)) {
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
  function n(u) {
    o(u(e));
  }
  function l(u, c = N) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (i = t(o, n) || N), u(e), () => {
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
  getContext: z,
  setContext: E
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = h({});
  return E($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = oe(), i = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    i.slotKey.set(c);
  }), se();
  const s = z(te), o = ((u = y(s)) == null ? void 0 : u.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...e,
    ...n
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
const X = "$$ms-gr-antd-slot-key";
function se() {
  E(X, h(void 0));
}
function oe() {
  return z(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: e,
  index: t,
  subIndex: i
}) {
  return E(Y, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(i)
  });
}
function qe() {
  return z(Y);
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
        var u = arguments[l];
        u && (n = o(n, s(u)));
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
      for (var u in n)
        t.call(n, u) && n[u] && (l = o(l, u));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(D);
var re = D.exports;
const M = /* @__PURE__ */ le(re), {
  getContext: ue,
  setContext: ce
} = window.__gradio__svelte__internal;
function ae(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((l, u) => (l[u] = h([]), l), {});
    return ce(t, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = ue(t);
    return function(l, u, c) {
      o && (l ? o[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : n.includes("default") && o.default.update((f) => {
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
  getSetItemFn: Ve
} = ae("checkbox-group"), {
  SvelteComponent: _e,
  assign: me,
  check_outros: de,
  component_subscribe: v,
  create_component: pe,
  create_slot: be,
  destroy_component: he,
  detach: G,
  empty: L,
  flush: b,
  get_all_dirty_from_scope: ge,
  get_slot_changes: ye,
  get_spread_object: R,
  get_spread_update: we,
  group_outros: ke,
  handle_promise: Ce,
  init: ve,
  insert: Z,
  mount_component: Se,
  noop: d,
  safe_not_equal: Ke,
  transition_in: k,
  transition_out: S,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function U(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ze,
    then: je,
    catch: xe,
    value: 24,
    blocks: [, , ,]
  };
  return Ce(
    /*AwaitedCheckboxGroup*/
    e[5],
    s
  ), {
    c() {
      t = L(), s.block.c();
    },
    m(o, n) {
      Z(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, n) {
      e = o, Ie(s, e, n);
    },
    i(o) {
      i || (k(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        S(l);
      }
      i = !1;
    },
    d(o) {
      o && G(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function xe(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function je(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: M(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-checkbox-group"
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
    F(
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
      default: [Ne]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = me(o, s[n]);
  return t = new /*CheckboxGroup*/
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
      const u = l & /*$mergedProps, $slots, $options, $children, value*/
      31 ? we(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: M(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-checkbox-group"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && R(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && R(F(
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
      4194304 && (u.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(u);
    },
    i(n) {
      i || (k(t.$$.fragment, n), i = !0);
    },
    o(n) {
      S(t.$$.fragment, n), i = !1;
    },
    d(n) {
      he(t, n);
    }
  };
}
function Ne(e) {
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
      t || (k(s, o), t = !0);
    },
    o(o) {
      S(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function ze(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Ee(e) {
  let t, i, s = (
    /*$mergedProps*/
    e[1].visible && U(e)
  );
  return {
    c() {
      s && s.c(), t = L();
    },
    m(o, n) {
      s && s.m(o, n), Z(o, t, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && k(s, 1)) : (s = U(o), s.c(), k(s, 1), s.m(t.parentNode, t)) : s && (ke(), S(s, 1, 1, () => {
        s = null;
      }), de());
    },
    i(o) {
      i || (k(s), i = !0);
    },
    o(o) {
      S(s), i = !1;
    },
    d(o) {
      o && G(t), s && s.d(o);
    }
  };
}
function Oe(e, t, i) {
  let s, o, n, l, u, {
    $$slots: c = {},
    $$scope: f
  } = t;
  const _ = Q(() => import("./checkbox.group-B4rG6drm.js"));
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
    value: C
  } = t, {
    as_item: K
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: P = ""
  } = t, {
    elem_classes: x = []
  } = t, {
    elem_style: j = {}
  } = t;
  const [O, B] = ne({
    gradio: m,
    props: s,
    _internal: g,
    visible: I,
    elem_id: P,
    elem_classes: x,
    elem_style: j,
    as_item: K,
    value: C
  });
  v(e, O, (r) => i(1, o = r));
  const q = ee();
  v(e, q, (r) => i(2, n = r));
  const {
    default: V,
    options: A
  } = fe(["default", "options"]);
  v(e, V, (r) => i(4, u = r)), v(e, A, (r) => i(3, l = r));
  const H = (r) => {
    i(0, C = r);
  };
  return e.$$set = (r) => {
    "gradio" in r && i(11, m = r.gradio), "props" in r && i(12, p = r.props), "_internal" in r && i(13, g = r._internal), "value" in r && i(0, C = r.value), "as_item" in r && i(14, K = r.as_item), "visible" in r && i(15, I = r.visible), "elem_id" in r && i(16, P = r.elem_id), "elem_classes" in r && i(17, x = r.elem_classes), "elem_style" in r && i(18, j = r.elem_style), "$$scope" in r && i(22, f = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && a.update((r) => ({
      ...r,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    1042433 && B({
      gradio: m,
      props: s,
      _internal: g,
      visible: I,
      elem_id: P,
      elem_classes: x,
      elem_style: j,
      as_item: K,
      value: C
    });
  }, [C, o, n, l, u, _, a, O, q, V, A, m, p, g, K, I, P, x, j, s, c, H, f];
}
class Ae extends _e {
  constructor(t) {
    super(), ve(this, t, Oe, Ee, Ke, {
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
  Ae as I,
  qe as g,
  h as w
};
