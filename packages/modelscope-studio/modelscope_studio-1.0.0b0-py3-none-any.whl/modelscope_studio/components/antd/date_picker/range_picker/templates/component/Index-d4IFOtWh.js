async function G() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(t) {
  return await G(), t().then((e) => e.default);
}
function V(t) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = t;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), f = (...m) => {
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
        return e.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
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
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, o;
      }
      const _ = u[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function N() {
}
function J(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Q(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return N;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return Q(t, (i) => e = i)(), e;
}
const k = [];
function h(t, e = N) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (J(t, c) && (t = c, i)) {
      const u = !k.length;
      for (const f of s)
        f[1](), k.push(f, t);
      if (u) {
        for (let f = 0; f < k.length; f += 2)
          k[f][0](k[f + 1]);
        k.length = 0;
      }
    }
  }
  function n(c) {
    o(c(t));
  }
  function l(c, u = N) {
    const f = [c, u];
    return s.add(f), s.size === 1 && (i = e(o, n) || N), c(t), () => {
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
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const t = h({});
  return E(T, t);
}
const $ = "$$ms-gr-antd-context-key";
function ee(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ne(), i = se({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((u) => {
    i.slotKey.set(u);
  }), te();
  const s = z($), o = ((c = y(s)) == null ? void 0 : c.as_item) || t.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...t,
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
const R = "$$ms-gr-antd-slot-key";
function te() {
  E(R, h(void 0));
}
function ne() {
  return z(R);
}
const D = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: t,
  index: e,
  subIndex: i
}) {
  return E(D, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function Oe() {
  return z(D);
}
function oe(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var U = {
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
        e.call(n, c) && n[c] && (l = o(l, c));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(U);
var ie = U.exports;
const A = /* @__PURE__ */ oe(ie), {
  getContext: le,
  setContext: re
} = window.__gradio__svelte__internal;
function ce(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((l, c) => (l[c] = h([]), l), {});
    return re(e, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = le(e);
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
  getItems: ue,
  getSetItemFn: qe
} = ce("date-picker"), {
  SvelteComponent: ae,
  assign: fe,
  check_outros: _e,
  component_subscribe: j,
  create_component: me,
  create_slot: de,
  destroy_component: pe,
  detach: X,
  empty: Y,
  flush: p,
  get_all_dirty_from_scope: be,
  get_slot_changes: ge,
  get_spread_object: F,
  get_spread_update: he,
  group_outros: ye,
  handle_promise: ke,
  init: we,
  insert: L,
  mount_component: Ce,
  noop: d,
  safe_not_equal: ve,
  transition_in: w,
  transition_out: C,
  update_await_block_branch: Se,
  update_slot_base: Ke
} = window.__gradio__svelte__internal;
function M(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ne,
    then: Pe,
    catch: Ie,
    value: 22,
    blocks: [, , ,]
  };
  return ke(
    /*AwaitedDatePickerRangePicker*/
    t[4],
    s
  ), {
    c() {
      e = Y(), s.block.c();
    },
    m(o, n) {
      L(o, e, n), s.block.m(o, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, i = !0;
    },
    p(o, n) {
      t = o, Se(s, t, n);
    },
    i(o) {
      i || (w(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        C(l);
      }
      i = !1;
    },
    d(o) {
      o && X(e), s.block.d(o), s.token = null, s = null;
    }
  };
}
function Ie(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Pe(t) {
  let e, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[1].elem_style
      )
    },
    {
      className: A(
        /*$mergedProps*/
        t[1].elem_classes,
        "ms-gr-antd-date-picker-range-picker"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[1].elem_id
      )
    },
    /*$mergedProps*/
    t[1].props,
    V(
      /*$mergedProps*/
      t[1]
    ),
    {
      slots: (
        /*$slots*/
        t[2]
      )
    },
    {
      value: (
        /*$mergedProps*/
        t[1].props.value || /*$mergedProps*/
        t[1].value
      )
    },
    {
      presetItems: (
        /*$presets*/
        t[3]
      )
    },
    {
      onValueChange: (
        /*func*/
        t[19]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [je]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = fe(o, s[n]);
  return e = new /*DateRangePicker*/
  t[22]({
    props: o
  }), {
    c() {
      me(e.$$.fragment);
    },
    m(n, l) {
      Ce(e, n, l), i = !0;
    },
    p(n, l) {
      const c = l & /*$mergedProps, $slots, $presets, value*/
      15 ? he(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-date-picker-range-picker"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && F(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && F(V(
        /*$mergedProps*/
        n[1]
      )), l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          n[1].props.value || /*$mergedProps*/
          n[1].value
        )
      }, l & /*$presets*/
      8 && {
        presetItems: (
          /*$presets*/
          n[3]
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[19]
        )
      }]) : {};
      l & /*$$scope*/
      1048576 && (c.$$scope = {
        dirty: l,
        ctx: n
      }), e.$set(c);
    },
    i(n) {
      i || (w(e.$$.fragment, n), i = !0);
    },
    o(n) {
      C(e.$$.fragment, n), i = !1;
    },
    d(n) {
      pe(e, n);
    }
  };
}
function je(t) {
  let e;
  const i = (
    /*#slots*/
    t[18].default
  ), s = de(
    i,
    t,
    /*$$scope*/
    t[20],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, n) {
      s && s.m(o, n), e = !0;
    },
    p(o, n) {
      s && s.p && (!e || n & /*$$scope*/
      1048576) && Ke(
        s,
        i,
        o,
        /*$$scope*/
        o[20],
        e ? ge(
          i,
          /*$$scope*/
          o[20],
          n,
          null
        ) : be(
          /*$$scope*/
          o[20]
        ),
        null
      );
    },
    i(o) {
      e || (w(s, o), e = !0);
    },
    o(o) {
      C(s, o), e = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ne(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function ze(t) {
  let e, i, s = (
    /*$mergedProps*/
    t[1].visible && M(t)
  );
  return {
    c() {
      s && s.c(), e = Y();
    },
    m(o, n) {
      s && s.m(o, n), L(o, e, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && w(s, 1)) : (s = M(o), s.c(), w(s, 1), s.m(e.parentNode, e)) : s && (ye(), C(s, 1, 1, () => {
        s = null;
      }), _e());
    },
    i(o) {
      i || (w(s), i = !0);
    },
    o(o) {
      C(s), i = !1;
    },
    d(o) {
      o && X(e), s && s.d(o);
    }
  };
}
function Ee(t, e, i) {
  let s, o, n, l, {
    $$slots: c = {},
    $$scope: u
  } = e;
  const f = H(() => import("./date-picker.range-picker-BZBQgISu.js"));
  let {
    gradio: _
  } = e, {
    props: m = {}
  } = e;
  const b = h(m);
  j(t, b, (r) => i(17, s = r));
  let {
    _internal: a = {}
  } = e, {
    value: g
  } = e, {
    as_item: v
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [O, Z] = ee({
    gradio: _,
    props: s,
    _internal: a,
    visible: S,
    elem_id: K,
    elem_classes: I,
    elem_style: P,
    as_item: v,
    value: g
  });
  j(t, O, (r) => i(1, o = r));
  const q = W();
  j(t, q, (r) => i(2, n = r));
  const {
    presets: x
  } = ue(["presets"]);
  j(t, x, (r) => i(3, l = r));
  const B = (r) => {
    i(0, g = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && i(9, _ = r.gradio), "props" in r && i(10, m = r.props), "_internal" in r && i(11, a = r._internal), "value" in r && i(0, g = r.value), "as_item" in r && i(12, v = r.as_item), "visible" in r && i(13, S = r.visible), "elem_id" in r && i(14, K = r.elem_id), "elem_classes" in r && i(15, I = r.elem_classes), "elem_style" in r && i(16, P = r.elem_style), "$$scope" in r && i(20, u = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    1024 && b.update((r) => ({
      ...r,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    260609 && Z({
      gradio: _,
      props: s,
      _internal: a,
      visible: S,
      elem_id: K,
      elem_classes: I,
      elem_style: P,
      as_item: v,
      value: g
    });
  }, [g, o, n, l, f, b, O, q, x, _, m, a, v, S, K, I, P, s, c, B, u];
}
class xe extends ae {
  constructor(e) {
    super(), we(this, e, Ee, ze, ve, {
      gradio: 9,
      props: 10,
      _internal: 11,
      value: 0,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[9];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), p();
  }
  get props() {
    return this.$$.ctx[10];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[11];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
export {
  xe as I,
  Oe as g,
  h as w
};
