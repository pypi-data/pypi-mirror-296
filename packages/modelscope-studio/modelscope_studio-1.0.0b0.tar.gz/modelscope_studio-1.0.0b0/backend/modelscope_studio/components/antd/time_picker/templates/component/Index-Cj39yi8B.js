async function T() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function Z(t) {
  return await T(), t().then((e) => e.default);
}
function q(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((o, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const a = l[1], u = a.split("_"), f = (...m) => {
        const p = m.map((c) => m && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return e.dispatch(a.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        o[u[0]] = m;
        for (let c = 1; c < u.length - 1; c++) {
          const h = {
            ...n.props[u[c]] || {}
          };
          m[u[c]] = h, m = h;
        }
        const p = u[u.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, o;
      }
      const d = u[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function j() {
}
function B(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function G(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return j;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return G(t, (i) => e = i)(), e;
}
const k = [];
function g(t, e = j) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(a) {
    if (B(t, a) && (t = a, i)) {
      const u = !k.length;
      for (const f of n)
        f[1](), k.push(f, t);
      if (u) {
        for (let f = 0; f < k.length; f += 2)
          k[f][0](k[f + 1]);
        k.length = 0;
      }
    }
  }
  function s(a) {
    o(a(t));
  }
  function l(a, u = j) {
    const f = [a, u];
    return n.add(f), n.size === 1 && (i = e(o, s) || j), a(t), () => {
      n.delete(f), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: I
} = window.__gradio__svelte__internal, H = "$$ms-gr-antd-slots-key";
function J() {
  const t = g({});
  return I(H, t);
}
const Q = "$$ms-gr-antd-context-key";
function W(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ee(), i = te({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((u) => {
    i.slotKey.set(u);
  }), $();
  const n = z(Q), o = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? o ? y(n)[o] : y(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: f
    } = y(l);
    f && (u = u[f]), l.update((d) => ({
      ...d,
      ...u
    }));
  }), [l, (u) => {
    const f = u.as_item ? y(n)[u.as_item] : y(n);
    return l.set({
      ...u,
      ...f
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const R = "$$ms-gr-antd-slot-key";
function $() {
  I(R, g(void 0));
}
function ee() {
  return z(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function te({
  slot: t,
  index: e,
  subIndex: i
}) {
  return I(U, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(i)
  });
}
function Pe() {
  return z(U);
}
function ne(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var X = {
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
      for (var s = "", l = 0; l < arguments.length; l++) {
        var a = arguments[l];
        a && (s = o(s, n(a)));
      }
      return s;
    }
    function n(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var a in s)
        e.call(s, a) && s[a] && (l = o(l, a));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(X);
var se = X.exports;
const A = /* @__PURE__ */ ne(se), {
  SvelteComponent: ie,
  assign: oe,
  check_outros: le,
  component_subscribe: N,
  create_component: re,
  create_slot: ce,
  destroy_component: ue,
  detach: Y,
  empty: D,
  flush: b,
  get_all_dirty_from_scope: ae,
  get_slot_changes: fe,
  get_spread_object: x,
  get_spread_update: _e,
  group_outros: me,
  handle_promise: de,
  init: pe,
  insert: F,
  mount_component: be,
  noop: _,
  safe_not_equal: he,
  transition_in: w,
  transition_out: v,
  update_await_block_branch: ge,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function V(t) {
  let e, i, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ce,
    then: we,
    catch: ke,
    value: 20,
    blocks: [, , ,]
  };
  return de(
    /*AwaitedTimePicker*/
    t[3],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(o, s) {
      F(o, e, s), n.block.m(o, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, i = !0;
    },
    p(o, s) {
      t = o, ge(n, t, s);
    },
    i(o) {
      i || (w(n.block), i = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        v(l);
      }
      i = !1;
    },
    d(o) {
      o && Y(e), n.block.d(o), n.token = null, n = null;
    }
  };
}
function ke(t) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function we(t) {
  let e, i;
  const n = [
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
        "ms-gr-antd-time-picker"
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
    q(
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
      onValueChange: (
        /*func*/
        t[17]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [ve]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    o = oe(o, n[s]);
  return e = new /*TimePicker*/
  t[20]({
    props: o
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(s, l) {
      be(e, s, l), i = !0;
    },
    p(s, l) {
      const a = l & /*$mergedProps, $slots, value*/
      7 ? _e(n, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-time-picker"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && x(
        /*$mergedProps*/
        s[1].props
      ), l & /*$mergedProps*/
      2 && x(q(
        /*$mergedProps*/
        s[1]
      )), l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          s[1].props.value || /*$mergedProps*/
          s[1].value
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[17]
        )
      }]) : {};
      l & /*$$scope*/
      262144 && (a.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      i || (w(e.$$.fragment, s), i = !0);
    },
    o(s) {
      v(e.$$.fragment, s), i = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function ve(t) {
  let e;
  const i = (
    /*#slots*/
    t[16].default
  ), n = ce(
    i,
    t,
    /*$$scope*/
    t[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(o, s) {
      n && n.m(o, s), e = !0;
    },
    p(o, s) {
      n && n.p && (!e || s & /*$$scope*/
      262144) && ye(
        n,
        i,
        o,
        /*$$scope*/
        o[18],
        e ? fe(
          i,
          /*$$scope*/
          o[18],
          s,
          null
        ) : ae(
          /*$$scope*/
          o[18]
        ),
        null
      );
    },
    i(o) {
      e || (w(n, o), e = !0);
    },
    o(o) {
      v(n, o), e = !1;
    },
    d(o) {
      n && n.d(o);
    }
  };
}
function Ce(t) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function Ke(t) {
  let e, i, n = (
    /*$mergedProps*/
    t[1].visible && V(t)
  );
  return {
    c() {
      n && n.c(), e = D();
    },
    m(o, s) {
      n && n.m(o, s), F(o, e, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[1].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      2 && w(n, 1)) : (n = V(o), n.c(), w(n, 1), n.m(e.parentNode, e)) : n && (me(), v(n, 1, 1, () => {
        n = null;
      }), le());
    },
    i(o) {
      i || (w(n), i = !0);
    },
    o(o) {
      v(n), i = !1;
    },
    d(o) {
      o && Y(e), n && n.d(o);
    }
  };
}
function Se(t, e, i) {
  let n, o, s, {
    $$slots: l = {},
    $$scope: a
  } = e;
  const u = Z(() => import("./time-picker-B0ntKB-u.js"));
  let {
    gradio: f
  } = e, {
    props: d = {}
  } = e;
  const m = g(d);
  N(t, m, (r) => i(15, n = r));
  let {
    _internal: p = {}
  } = e, {
    value: c
  } = e, {
    as_item: h
  } = e, {
    visible: C = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [E, L] = W({
    gradio: f,
    props: n,
    _internal: p,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: h,
    value: c
  });
  N(t, E, (r) => i(1, o = r));
  const O = J();
  N(t, O, (r) => i(2, s = r));
  const M = (r) => {
    i(0, c = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && i(7, f = r.gradio), "props" in r && i(8, d = r.props), "_internal" in r && i(9, p = r._internal), "value" in r && i(0, c = r.value), "as_item" in r && i(10, h = r.as_item), "visible" in r && i(11, C = r.visible), "elem_id" in r && i(12, K = r.elem_id), "elem_classes" in r && i(13, S = r.elem_classes), "elem_style" in r && i(14, P = r.elem_style), "$$scope" in r && i(18, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && m.update((r) => ({
      ...r,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && L({
      gradio: f,
      props: n,
      _internal: p,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: h,
      value: c
    });
  }, [c, o, s, u, m, E, O, f, d, p, h, C, K, S, P, n, l, M, a];
}
class je extends ie {
  constructor(e) {
    super(), pe(this, e, Se, Ke, he, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 0,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), b();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  je as I,
  Pe as g,
  g as w
};
