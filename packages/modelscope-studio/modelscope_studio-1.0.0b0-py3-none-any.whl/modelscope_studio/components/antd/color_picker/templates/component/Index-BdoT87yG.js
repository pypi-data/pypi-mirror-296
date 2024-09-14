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
function V(e) {
  const {
    gradio: t,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const r = n.match(/bind_(.+)_event/);
    if (r) {
      const c = r[1], l = c.split("_"), f = (...m) => {
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
        return t.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (l.length > 1) {
        let m = {
          ...s.props[l[0]] || {}
        };
        o[l[0]] = m;
        for (let a = 1; a < l.length - 1; a++) {
          const d = {
            ...s.props[l[a]] || {}
          };
          m[l[a]] = d, m = d;
        }
        const b = l[l.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, o;
      }
      const _ = l[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function C() {
}
function T(e) {
  return e();
}
function W(e) {
  e.forEach(T);
}
function $(e) {
  return typeof e == "function";
}
function ee(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function U(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return C;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function w(e) {
  let t;
  return U(e, (i) => t = i)(), t;
}
const k = [];
function te(e, t) {
  return {
    subscribe: g(e, t).subscribe
  };
}
function g(e, t = C) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (ee(e, c) && (e = c, i)) {
      const l = !k.length;
      for (const f of s)
        f[1](), k.push(f, e);
      if (l) {
        for (let f = 0; f < k.length; f += 2)
          k[f][0](k[f + 1]);
        k.length = 0;
      }
    }
  }
  function n(c) {
    o(c(e));
  }
  function r(c, l = C) {
    const f = [c, l];
    return s.add(f), s.size === 1 && (i = t(o, n) || C), c(e), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: r
  };
}
function Fe(e, t, i) {
  const s = !Array.isArray(e), o = s ? [e] : e;
  if (!o.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const n = t.length < 2;
  return te(i, (r, c) => {
    let l = !1;
    const f = [];
    let _ = 0, m = C;
    const b = () => {
      if (_)
        return;
      m();
      const d = t(s ? f[0] : f, r, c);
      n ? r(d) : m = $(d) ? d : C;
    }, a = o.map((d, y) => U(d, (v) => {
      f[y] = v, _ &= ~(1 << y), l && b();
    }, () => {
      _ |= 1 << y;
    }));
    return l = !0, b(), function() {
      W(a), m(), l = !1;
    };
  });
}
const {
  getContext: z,
  setContext: x
} = window.__gradio__svelte__internal, ne = "$$ms-gr-antd-slots-key";
function se() {
  const e = g({});
  return x(ne, e);
}
const oe = "$$ms-gr-antd-context-key";
function ie(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = le(), i = ue({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    i.slotKey.set(l);
  }), re();
  const s = z(oe), o = ((c = w(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? w(s)[o] : w(s) : {}, r = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((l) => {
    const {
      as_item: f
    } = w(r);
    f && (l = l[f]), r.update((_) => ({
      ..._,
      ...l
    }));
  }), [r, (l) => {
    const f = l.as_item ? w(s)[l.as_item] : w(s);
    return r.set({
      ...l,
      ...f
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function re() {
  x(X, g(void 0));
}
function le() {
  return z(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function ue({
  slot: e,
  index: t,
  subIndex: i
}) {
  return x(Y, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(i)
  });
}
function Me() {
  return z(Y);
}
function ce(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var B = {
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
      for (var n = "", r = 0; r < arguments.length; r++) {
        var c = arguments[r];
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
      var r = "";
      for (var c in n)
        t.call(n, c) && n[c] && (r = o(r, c));
      return r;
    }
    function o(n, r) {
      return r ? n ? n + " " + r : n + r : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(B);
var ae = B.exports;
const F = /* @__PURE__ */ ce(ae), {
  getContext: fe,
  setContext: _e
} = window.__gradio__svelte__internal;
function me(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((r, c) => (r[c] = g([]), r), {});
    return _e(t, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = fe(t);
    return function(r, c, l) {
      o && (r ? o[r].update((f) => {
        const _ = [...f];
        return n.includes(r) ? _[c] = l : _[c] = void 0, _;
      }) : n.includes("default") && o.default.update((f) => {
        const _ = [...f];
        return _[c] = l, _;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: s
  };
}
const {
  getItems: de,
  getSetItemFn: Re
} = me("color-picker"), {
  SvelteComponent: pe,
  assign: be,
  check_outros: he,
  component_subscribe: N,
  create_component: ge,
  create_slot: ye,
  destroy_component: ve,
  detach: D,
  empty: L,
  flush: h,
  get_all_dirty_from_scope: we,
  get_slot_changes: ke,
  get_spread_object: M,
  get_spread_update: Ce,
  group_outros: Se,
  handle_promise: Ke,
  init: Ie,
  insert: Z,
  mount_component: Pe,
  noop: p,
  safe_not_equal: je,
  transition_in: S,
  transition_out: K,
  update_await_block_branch: Ee,
  update_slot_base: Ne
} = window.__gradio__svelte__internal;
function R(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Oe,
    then: xe,
    catch: ze,
    value: 23,
    blocks: [, , ,]
  };
  return Ke(
    /*AwaitedColorPicker*/
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
      e = o, Ee(s, e, n);
    },
    i(o) {
      i || (S(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const r = s.blocks[n];
        K(r);
      }
      i = !1;
    },
    d(o) {
      o && D(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function ze(e) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function xe(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[2].elem_style
      )
    },
    {
      className: F(
        /*$mergedProps*/
        e[2].elem_classes,
        "ms-gr-antd-color-picker"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[2].elem_id
      )
    },
    /*$mergedProps*/
    e[2].props,
    V(
      /*$mergedProps*/
      e[2]
    ),
    {
      value: (
        /*$mergedProps*/
        e[2].props.value ?? /*$mergedProps*/
        e[2].value
      )
    },
    {
      slots: (
        /*$slots*/
        e[3]
      )
    },
    {
      presetItems: (
        /*$presets*/
        e[4]
      )
    },
    {
      value_format: (
        /*value_format*/
        e[1]
      )
    },
    {
      onValueChange: (
        /*func*/
        e[20]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Ae]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = be(o, s[n]);
  return t = new /*ColorPicker*/
  e[23]({
    props: o
  }), {
    c() {
      ge(t.$$.fragment);
    },
    m(n, r) {
      Pe(t, n, r), i = !0;
    },
    p(n, r) {
      const c = r & /*$mergedProps, $slots, $presets, value_format, value*/
      31 ? Ce(s, [r & /*$mergedProps*/
      4 && {
        style: (
          /*$mergedProps*/
          n[2].elem_style
        )
      }, r & /*$mergedProps*/
      4 && {
        className: F(
          /*$mergedProps*/
          n[2].elem_classes,
          "ms-gr-antd-color-picker"
        )
      }, r & /*$mergedProps*/
      4 && {
        id: (
          /*$mergedProps*/
          n[2].elem_id
        )
      }, r & /*$mergedProps*/
      4 && M(
        /*$mergedProps*/
        n[2].props
      ), r & /*$mergedProps*/
      4 && M(V(
        /*$mergedProps*/
        n[2]
      )), r & /*$mergedProps*/
      4 && {
        value: (
          /*$mergedProps*/
          n[2].props.value ?? /*$mergedProps*/
          n[2].value
        )
      }, r & /*$slots*/
      8 && {
        slots: (
          /*$slots*/
          n[3]
        )
      }, r & /*$presets*/
      16 && {
        presetItems: (
          /*$presets*/
          n[4]
        )
      }, r & /*value_format*/
      2 && {
        value_format: (
          /*value_format*/
          n[1]
        )
      }, r & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[20]
        )
      }]) : {};
      r & /*$$scope*/
      2097152 && (c.$$scope = {
        dirty: r,
        ctx: n
      }), t.$set(c);
    },
    i(n) {
      i || (S(t.$$.fragment, n), i = !0);
    },
    o(n) {
      K(t.$$.fragment, n), i = !1;
    },
    d(n) {
      ve(t, n);
    }
  };
}
function Ae(e) {
  let t;
  const i = (
    /*#slots*/
    e[19].default
  ), s = ye(
    i,
    e,
    /*$$scope*/
    e[21],
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
      2097152) && Ne(
        s,
        i,
        o,
        /*$$scope*/
        o[21],
        t ? ke(
          i,
          /*$$scope*/
          o[21],
          n,
          null
        ) : we(
          /*$$scope*/
          o[21]
        ),
        null
      );
    },
    i(o) {
      t || (S(s, o), t = !0);
    },
    o(o) {
      K(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Oe(e) {
  return {
    c: p,
    m: p,
    p,
    i: p,
    o: p,
    d: p
  };
}
function qe(e) {
  let t, i, s = (
    /*$mergedProps*/
    e[2].visible && R(e)
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
      o[2].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      4 && S(s, 1)) : (s = R(o), s.c(), S(s, 1), s.m(t.parentNode, t)) : s && (Se(), K(s, 1, 1, () => {
        s = null;
      }), he());
    },
    i(o) {
      i || (S(s), i = !0);
    },
    o(o) {
      K(s), i = !1;
    },
    d(o) {
      o && D(t), s && s.d(o);
    }
  };
}
function Ve(e, t, i) {
  let s, o, n, r, {
    $$slots: c = {},
    $$scope: l
  } = t;
  const f = Q(() => import("./color-picker-CEkZuoEv.js"));
  let {
    gradio: _
  } = t, {
    props: m = {}
  } = t;
  const b = g(m);
  N(e, b, (u) => i(18, s = u));
  let {
    _internal: a = {}
  } = t, {
    value: d
  } = t, {
    value_format: y = "hex"
  } = t, {
    as_item: v
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: P = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: E = {}
  } = t;
  const [A, G] = ie({
    gradio: _,
    props: s,
    _internal: a,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: E,
    as_item: v,
    value: d
  });
  N(e, A, (u) => i(2, o = u));
  const O = se();
  N(e, O, (u) => i(3, n = u));
  const {
    presets: q
  } = de(["presets"]);
  N(e, q, (u) => i(4, r = u));
  const H = (u) => {
    i(0, d = u);
  };
  return e.$$set = (u) => {
    "gradio" in u && i(10, _ = u.gradio), "props" in u && i(11, m = u.props), "_internal" in u && i(12, a = u._internal), "value" in u && i(0, d = u.value), "value_format" in u && i(1, y = u.value_format), "as_item" in u && i(13, v = u.as_item), "visible" in u && i(14, I = u.visible), "elem_id" in u && i(15, P = u.elem_id), "elem_classes" in u && i(16, j = u.elem_classes), "elem_style" in u && i(17, E = u.elem_style), "$$scope" in u && i(21, l = u.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    2048 && b.update((u) => ({
      ...u,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    521217 && G({
      gradio: _,
      props: s,
      _internal: a,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: E,
      as_item: v,
      value: d
    });
  }, [d, y, o, n, r, f, b, A, O, q, _, m, a, v, I, P, j, E, s, c, H, l];
}
class Ue extends pe {
  constructor(t) {
    super(), Ie(this, t, Ve, qe, je, {
      gradio: 10,
      props: 11,
      _internal: 12,
      value: 0,
      value_format: 1,
      as_item: 13,
      visible: 14,
      elem_id: 15,
      elem_classes: 16,
      elem_style: 17
    });
  }
  get gradio() {
    return this.$$.ctx[10];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), h();
  }
  get props() {
    return this.$$.ctx[11];
  }
  set props(t) {
    this.$$set({
      props: t
    }), h();
  }
  get _internal() {
    return this.$$.ctx[12];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), h();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), h();
  }
  get value_format() {
    return this.$$.ctx[1];
  }
  set value_format(t) {
    this.$$set({
      value_format: t
    }), h();
  }
  get as_item() {
    return this.$$.ctx[13];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), h();
  }
  get visible() {
    return this.$$.ctx[14];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[15];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[16];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[17];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), h();
  }
}
export {
  Ue as I,
  w as a,
  Fe as d,
  Me as g,
  g as w
};
