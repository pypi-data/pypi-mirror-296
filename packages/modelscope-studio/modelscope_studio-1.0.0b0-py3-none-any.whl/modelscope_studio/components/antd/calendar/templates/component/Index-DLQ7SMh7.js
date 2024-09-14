async function Z() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function B(t) {
  return await Z(), t().then((e) => e.default);
}
function q(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((l, s) => {
    const i = s.match(/bind_(.+)_event/);
    if (i) {
      const a = i[1], u = a.split("_"), f = (...m) => {
        const b = m.map((c) => m && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
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
          payload: b,
          component: n
        });
      };
      if (u.length > 1) {
        let m = {
          ...n.props[u[0]] || {}
        };
        l[u[0]] = m;
        for (let c = 1; c < u.length - 1; c++) {
          const h = {
            ...n.props[u[c]] || {}
          };
          m[u[c]] = h, m = h;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, l;
      }
      const d = u[0];
      l[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return l;
  }, {});
}
function j() {
}
function G(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function H(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return j;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return H(t, (o) => e = o)(), e;
}
const w = [];
function g(t, e = j) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function l(a) {
    if (G(t, a) && (t = a, o)) {
      const u = !w.length;
      for (const f of n)
        f[1](), w.push(f, t);
      if (u) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function s(a) {
    l(a(t));
  }
  function i(a, u = j) {
    const f = [a, u];
    return n.add(f), n.size === 1 && (o = e(l, s) || j), a(t), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: l,
    update: s,
    subscribe: i
  };
}
const {
  getContext: z,
  setContext: I
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function Q() {
  const t = g({});
  return I(J, t);
}
const T = "$$ms-gr-antd-context-key";
function W(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ee(), o = te({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((u) => {
    o.slotKey.set(u);
  }), $();
  const n = z(T), l = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? l ? y(n)[l] : y(n) : {}, i = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((u) => {
    const {
      as_item: f
    } = y(i);
    f && (u = u[f]), i.update((d) => ({
      ...d,
      ...u
    }));
  }), [i, (u) => {
    const f = u.as_item ? y(n)[u.as_item] : y(n);
    return i.set({
      ...u,
      ...f
    });
  }]) : [i, (u) => {
    i.set(u);
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
  subIndex: o
}) {
  return I(U, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
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
    function o() {
      for (var s = "", i = 0; i < arguments.length; i++) {
        var a = arguments[i];
        a && (s = l(s, n(a)));
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
      var i = "";
      for (var a in s)
        e.call(s, a) && s[a] && (i = l(i, a));
      return i;
    }
    function l(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(X);
var se = X.exports;
const A = /* @__PURE__ */ ne(se), {
  SvelteComponent: oe,
  assign: le,
  check_outros: ie,
  component_subscribe: N,
  create_component: re,
  create_slot: ce,
  destroy_component: ue,
  detach: Y,
  empty: D,
  flush: p,
  get_all_dirty_from_scope: ae,
  get_slot_changes: fe,
  get_spread_object: x,
  get_spread_update: _e,
  group_outros: me,
  handle_promise: de,
  init: be,
  insert: F,
  mount_component: pe,
  noop: _,
  safe_not_equal: he,
  transition_in: v,
  transition_out: k,
  update_await_block_branch: ge,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function V(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ce,
    then: ve,
    catch: we,
    value: 20,
    blocks: [, , ,]
  };
  return de(
    /*AwaitedCalender*/
    t[3],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(l, s) {
      F(l, e, s), n.block.m(l, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(l, s) {
      t = l, ge(n, t, s);
    },
    i(l) {
      o || (v(n.block), o = !0);
    },
    o(l) {
      for (let s = 0; s < 3; s += 1) {
        const i = n.blocks[s];
        k(i);
      }
      o = !1;
    },
    d(l) {
      l && Y(e), n.block.d(l), n.token = null, n = null;
    }
  };
}
function we(t) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function ve(t) {
  let e, o;
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
        "ms-gr-antd-calender"
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
  let l = {
    $$slots: {
      default: [ke]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    l = le(l, n[s]);
  return e = new /*Calender*/
  t[20]({
    props: l
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(s, i) {
      pe(e, s, i), o = !0;
    },
    p(s, i) {
      const a = i & /*$mergedProps, $slots, value*/
      7 ? _e(n, [i & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, i & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-calender"
        )
      }, i & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, i & /*$mergedProps*/
      2 && x(
        /*$mergedProps*/
        s[1].props
      ), i & /*$mergedProps*/
      2 && x(q(
        /*$mergedProps*/
        s[1]
      )), i & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, i & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          s[1].props.value || /*$mergedProps*/
          s[1].value
        )
      }, i & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[17]
        )
      }]) : {};
      i & /*$$scope*/
      262144 && (a.$$scope = {
        dirty: i,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      o || (v(e.$$.fragment, s), o = !0);
    },
    o(s) {
      k(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function ke(t) {
  let e;
  const o = (
    /*#slots*/
    t[16].default
  ), n = ce(
    o,
    t,
    /*$$scope*/
    t[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(l, s) {
      n && n.m(l, s), e = !0;
    },
    p(l, s) {
      n && n.p && (!e || s & /*$$scope*/
      262144) && ye(
        n,
        o,
        l,
        /*$$scope*/
        l[18],
        e ? fe(
          o,
          /*$$scope*/
          l[18],
          s,
          null
        ) : ae(
          /*$$scope*/
          l[18]
        ),
        null
      );
    },
    i(l) {
      e || (v(n, l), e = !0);
    },
    o(l) {
      k(n, l), e = !1;
    },
    d(l) {
      n && n.d(l);
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
  let e, o, n = (
    /*$mergedProps*/
    t[1].visible && V(t)
  );
  return {
    c() {
      n && n.c(), e = D();
    },
    m(l, s) {
      n && n.m(l, s), F(l, e, s), o = !0;
    },
    p(l, [s]) {
      /*$mergedProps*/
      l[1].visible ? n ? (n.p(l, s), s & /*$mergedProps*/
      2 && v(n, 1)) : (n = V(l), n.c(), v(n, 1), n.m(e.parentNode, e)) : n && (me(), k(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(l) {
      o || (v(n), o = !0);
    },
    o(l) {
      k(n), o = !1;
    },
    d(l) {
      l && Y(e), n && n.d(l);
    }
  };
}
function Se(t, e, o) {
  let n, l, s, {
    $$slots: i = {},
    $$scope: a
  } = e;
  const u = B(() => import("./calendar-BIdzqtyR.js"));
  let {
    gradio: f
  } = e, {
    props: d = {}
  } = e;
  const m = g(d);
  N(t, m, (r) => o(15, n = r));
  let {
    _internal: b = {}
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
    _internal: b,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: h,
    value: c
  });
  N(t, E, (r) => o(1, l = r));
  const O = Q();
  N(t, O, (r) => o(2, s = r));
  const M = (r) => {
    o(0, c = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && o(7, f = r.gradio), "props" in r && o(8, d = r.props), "_internal" in r && o(9, b = r._internal), "value" in r && o(0, c = r.value), "as_item" in r && o(10, h = r.as_item), "visible" in r && o(11, C = r.visible), "elem_id" in r && o(12, K = r.elem_id), "elem_classes" in r && o(13, S = r.elem_classes), "elem_style" in r && o(14, P = r.elem_style), "$$scope" in r && o(18, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    256 && m.update((r) => ({
      ...r,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && L({
      gradio: f,
      props: n,
      _internal: b,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: h,
      value: c
    });
  }, [c, l, s, u, m, E, O, f, d, b, h, C, K, S, P, n, i, M, a];
}
class je extends oe {
  constructor(e) {
    super(), be(this, e, Se, Ke, he, {
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
    }), p();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[9];
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
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
export {
  je as I,
  Pe as g,
  g as w
};
