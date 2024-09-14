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
      const a = l[1], c = a.split("_"), _ = (...m) => {
        const h = m.map((u) => m && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
          payload: h,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let u = 1; u < c.length - 1; u++) {
          const g = {
            ...n.props[c[u]] || {}
          };
          m[c[u]] = g, m = g;
        }
        const h = c[c.length - 1];
        return m[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = _, i;
      }
      const b = c[0];
      i[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _;
    }
    return i;
  }, {});
}
function I() {
}
function T(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function W(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return I;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return W(t, (o) => e = o)(), e;
}
const k = [];
function p(t, e = I) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(a) {
    if (T(t, a) && (t = a, o)) {
      const c = !k.length;
      for (const _ of n)
        _[1](), k.push(_, t);
      if (c) {
        for (let _ = 0; _ < k.length; _ += 2)
          k[_][0](k[_ + 1]);
        k.length = 0;
      }
    }
  }
  function s(a) {
    i(a(t));
  }
  function l(a, c = I) {
    const _ = [a, c];
    return n.add(_), n.size === 1 && (o = e(i, s) || I), a(t), () => {
      n.delete(_), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
const {
  getContext: O,
  setContext: q
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const t = p({});
  return q($, t);
}
const te = "$$ms-gr-antd-context-key";
function ne(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = oe(), o = ie({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    o.slotKey.set(c);
  }), se();
  const n = O(te), i = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = p({
    ...t,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: _
    } = y(l);
    _ && (c = c[_]), l.update((b) => ({
      ...b,
      ...c
    }));
  }), [l, (c) => {
    const _ = c.as_item ? y(n)[c.as_item] : y(n);
    return l.set({
      ...c,
      ..._
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const B = "$$ms-gr-antd-slot-key";
function se() {
  q(B, p(void 0));
}
function oe() {
  return O(B);
}
const D = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: t,
  index: e,
  subIndex: o
}) {
  return q(D, {
    slotKey: p(t),
    slotIndex: p(e),
    subSlotIndex: p(o)
  });
}
function ze() {
  return O(D);
}
function le(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var F = {
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
        var a = arguments[l];
        a && (s = i(s, n(a)));
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
      for (var a in s)
        e.call(s, a) && s[a] && (l = i(l, a));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(F);
var re = F.exports;
const U = /* @__PURE__ */ le(re), {
  SvelteComponent: ue,
  assign: ce,
  check_outros: ae,
  component_subscribe: E,
  create_component: _e,
  create_slot: fe,
  destroy_component: de,
  detach: L,
  empty: M,
  flush: f,
  get_all_dirty_from_scope: me,
  get_slot_changes: be,
  get_spread_object: X,
  get_spread_update: he,
  group_outros: ge,
  handle_promise: pe,
  init: ye,
  insert: Z,
  mount_component: ke,
  noop: d,
  safe_not_equal: we,
  transition_in: w,
  transition_out: v,
  update_await_block_branch: ve,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function Y(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: je,
    then: Se,
    catch: Ke,
    value: 24,
    blocks: [, , ,]
  };
  return pe(
    /*AwaitedRadioButton*/
    t[3],
    n
  ), {
    c() {
      e = M(), n.block.c();
    },
    m(i, s) {
      Z(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, ve(n, t, s);
    },
    i(i) {
      o || (w(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        v(l);
      }
      o = !1;
    },
    d(i) {
      i && L(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function Ke(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Se(t) {
  let e, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[1].elem_style
      )
    },
    {
      className: U(
        /*$mergedProps*/
        t[1].elem_classes,
        "ms-gr-antd-radio-button"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[1].elem_id
      )
    },
    {
      checked: (
        /*$mergedProps*/
        t[1].value
      )
    },
    {
      value: (
        /*$mergedProps*/
        t[1].group_value
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
      onValueChange: (
        /*func*/
        t[21]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Pe]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = ce(i, n[s]);
  return e = new /*RadioButton*/
  t[24]({
    props: i
  }), {
    c() {
      _e(e.$$.fragment);
    },
    m(s, l) {
      ke(e, s, l), o = !0;
    },
    p(s, l) {
      const a = l & /*$mergedProps, $slots, value*/
      7 ? he(n, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: U(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-radio-button"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && {
        checked: (
          /*$mergedProps*/
          s[1].value
        )
      }, l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          s[1].group_value
        )
      }, l & /*$mergedProps*/
      2 && X(
        /*$mergedProps*/
        s[1].props
      ), l & /*$mergedProps*/
      2 && X(V(
        /*$mergedProps*/
        s[1]
      )), l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[21]
        )
      }]) : {};
      l & /*$$scope*/
      4194304 && (a.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      o || (w(e.$$.fragment, s), o = !0);
    },
    o(s) {
      v(e.$$.fragment, s), o = !1;
    },
    d(s) {
      de(e, s);
    }
  };
}
function Pe(t) {
  let e;
  const o = (
    /*#slots*/
    t[20].default
  ), n = fe(
    o,
    t,
    /*$$scope*/
    t[22],
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
      4194304) && Ce(
        n,
        o,
        i,
        /*$$scope*/
        i[22],
        e ? be(
          o,
          /*$$scope*/
          i[22],
          s,
          null
        ) : me(
          /*$$scope*/
          i[22]
        ),
        null
      );
    },
    i(i) {
      e || (w(n, i), e = !0);
    },
    o(i) {
      v(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function je(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Ne(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[1].visible && Y(t)
  );
  return {
    c() {
      n && n.c(), e = M();
    },
    m(i, s) {
      n && n.m(i, s), Z(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      2 && w(n, 1)) : (n = Y(i), n.c(), w(n, 1), n.m(e.parentNode, e)) : n && (ge(), v(n, 1, 1, () => {
        n = null;
      }), ae());
    },
    i(i) {
      o || (w(n), o = !0);
    },
    o(i) {
      v(n), o = !1;
    },
    d(i) {
      i && L(e), n && n.d(i);
    }
  };
}
function xe(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: a
  } = e;
  const c = Q(() => import("./radio.button-Cd7RYGd2.js"));
  let {
    gradio: _
  } = e, {
    props: b = {}
  } = e;
  const m = p(b);
  E(t, m, (r) => o(19, n = r));
  let {
    _internal: h = {}
  } = e, {
    value: u
  } = e, {
    group_value: g
  } = e, {
    auto_focus: C
  } = e, {
    default_checked: K
  } = e, {
    disabled: S
  } = e, {
    as_item: P
  } = e, {
    visible: j = !0
  } = e, {
    elem_id: N = ""
  } = e, {
    elem_classes: x = []
  } = e, {
    elem_style: z = {}
  } = e;
  const [A, G] = ne({
    gradio: _,
    props: n,
    _internal: h,
    visible: j,
    elem_id: N,
    elem_classes: x,
    elem_style: z,
    as_item: P,
    value: u,
    auto_focus: C,
    group_value: g,
    default_checked: K,
    disabled: S
  });
  E(t, A, (r) => o(1, i = r));
  const R = ee();
  E(t, R, (r) => o(2, s = r));
  const H = (r) => {
    o(0, u = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && o(7, _ = r.gradio), "props" in r && o(8, b = r.props), "_internal" in r && o(9, h = r._internal), "value" in r && o(0, u = r.value), "group_value" in r && o(10, g = r.group_value), "auto_focus" in r && o(11, C = r.auto_focus), "default_checked" in r && o(12, K = r.default_checked), "disabled" in r && o(13, S = r.disabled), "as_item" in r && o(14, P = r.as_item), "visible" in r && o(15, j = r.visible), "elem_id" in r && o(16, N = r.elem_id), "elem_classes" in r && o(17, x = r.elem_classes), "elem_style" in r && o(18, z = r.elem_style), "$$scope" in r && o(22, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && m.update((r) => ({
      ...r,
      ...b
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, auto_focus, group_value, default_checked, disabled*/
    1048193 && G({
      gradio: _,
      props: n,
      _internal: h,
      visible: j,
      elem_id: N,
      elem_classes: x,
      elem_style: z,
      as_item: P,
      value: u,
      auto_focus: C,
      group_value: g,
      default_checked: K,
      disabled: S
    });
  }, [u, i, s, c, m, A, R, _, b, h, g, C, K, S, P, j, N, x, z, n, l, H, a];
}
class Ie extends ue {
  constructor(e) {
    super(), ye(this, e, xe, Ne, we, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 0,
      group_value: 10,
      auto_focus: 11,
      default_checked: 12,
      disabled: 13,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), f();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), f();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), f();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), f();
  }
  get group_value() {
    return this.$$.ctx[10];
  }
  set group_value(e) {
    this.$$set({
      group_value: e
    }), f();
  }
  get auto_focus() {
    return this.$$.ctx[11];
  }
  set auto_focus(e) {
    this.$$set({
      auto_focus: e
    }), f();
  }
  get default_checked() {
    return this.$$.ctx[12];
  }
  set default_checked(e) {
    this.$$set({
      default_checked: e
    }), f();
  }
  get disabled() {
    return this.$$.ctx[13];
  }
  set disabled(e) {
    this.$$set({
      disabled: e
    }), f();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), f();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), f();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), f();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), f();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), f();
  }
}
export {
  Ie as I,
  ze as g,
  p as w
};
