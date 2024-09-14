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
function O(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const a = l[1], u = a.split("_"), f = (...m) => {
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
        i[u[0]] = m;
        for (let c = 1; c < u.length - 1; c++) {
          const p = {
            ...n.props[u[c]] || {}
          };
          m[u[c]] = p, m = p;
        }
        const b = u[u.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const d = u[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function x() {
}
function G(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function H(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return x;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return H(t, (o) => e = o)(), e;
}
const k = [];
function g(t, e = x) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(a) {
    if (G(t, a) && (t = a, o)) {
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
    i(a(t));
  }
  function l(a, u = x) {
    const f = [a, u];
    return n.add(f), n.size === 1 && (o = e(i, s) || x), a(t), () => {
      n.delete(f), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: l
  };
}
const {
  getContext: N,
  setContext: z
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function Q() {
  const t = g({});
  return z(J, t);
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
  const n = N(T), i = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = g({
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
  z(R, g(void 0));
}
function ee() {
  return N(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function te({
  slot: t,
  index: e,
  subIndex: o
}) {
  return z(U, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function Pe() {
  return N(U);
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
})(X);
var se = X.exports;
const q = /* @__PURE__ */ ne(se), {
  SvelteComponent: oe,
  assign: ie,
  check_outros: le,
  component_subscribe: j,
  create_component: re,
  create_slot: ce,
  destroy_component: ue,
  detach: Y,
  empty: D,
  flush: h,
  get_all_dirty_from_scope: ae,
  get_slot_changes: fe,
  get_spread_object: A,
  get_spread_update: _e,
  group_outros: me,
  handle_promise: de,
  init: be,
  insert: F,
  mount_component: he,
  noop: _,
  safe_not_equal: pe,
  transition_in: w,
  transition_out: C,
  update_await_block_branch: ge,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function V(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ve,
    then: we,
    catch: ke,
    value: 20,
    blocks: [, , ,]
  };
  return de(
    /*AwaitedCheckbox*/
    t[3],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(i, s) {
      F(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, ge(n, t, s);
    },
    i(i) {
      o || (w(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        C(l);
      }
      o = !1;
    },
    d(i) {
      i && Y(e), n.block.d(i), n.token = null, n = null;
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
  let e, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[1].elem_style
      )
    },
    {
      className: q(
        /*$mergedProps*/
        t[1].elem_classes,
        "ms-gr-antd-checkbox"
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
    O(
      /*$mergedProps*/
      t[1]
    ),
    {
      checked: (
        /*$mergedProps*/
        t[1].props.checked ?? /*$mergedProps*/
        t[1].value
      )
    },
    {
      slots: (
        /*$slots*/
        t[2]
      )
    },
    {
      onValueChange: (
        /*func*/
        t[17]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Ce]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = ie(i, n[s]);
  return e = new /*Checkbox*/
  t[20]({
    props: i
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(s, l) {
      he(e, s, l), o = !0;
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
        className: q(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-checkbox"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && A(
        /*$mergedProps*/
        s[1].props
      ), l & /*$mergedProps*/
      2 && A(O(
        /*$mergedProps*/
        s[1]
      )), l & /*$mergedProps*/
      2 && {
        checked: (
          /*$mergedProps*/
          s[1].props.checked ?? /*$mergedProps*/
          s[1].value
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
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
      o || (w(e.$$.fragment, s), o = !0);
    },
    o(s) {
      C(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function Ce(t) {
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
    m(i, s) {
      n && n.m(i, s), e = !0;
    },
    p(i, s) {
      n && n.p && (!e || s & /*$$scope*/
      262144) && ye(
        n,
        o,
        i,
        /*$$scope*/
        i[18],
        e ? fe(
          o,
          /*$$scope*/
          i[18],
          s,
          null
        ) : ae(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      e || (w(n, i), e = !0);
    },
    o(i) {
      C(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function ve(t) {
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
    m(i, s) {
      n && n.m(i, s), F(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      2 && w(n, 1)) : (n = V(i), n.c(), w(n, 1), n.m(e.parentNode, e)) : n && (me(), C(n, 1, 1, () => {
        n = null;
      }), le());
    },
    i(i) {
      o || (w(n), o = !0);
    },
    o(i) {
      C(n), o = !1;
    },
    d(i) {
      i && Y(e), n && n.d(i);
    }
  };
}
function Se(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: a
  } = e;
  const u = B(() => import("./checkbox-DeB-THaj.js"));
  let {
    gradio: f
  } = e, {
    props: d = {}
  } = e;
  const m = g(d);
  j(t, m, (r) => o(15, n = r));
  let {
    _internal: b = {}
  } = e, {
    value: c
  } = e, {
    as_item: p
  } = e, {
    visible: v = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [I, L] = W({
    gradio: f,
    props: n,
    _internal: b,
    visible: v,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: p,
    value: c
  });
  j(t, I, (r) => o(1, i = r));
  const E = Q();
  j(t, E, (r) => o(2, s = r));
  const M = (r) => {
    o(0, c = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && o(7, f = r.gradio), "props" in r && o(8, d = r.props), "_internal" in r && o(9, b = r._internal), "value" in r && o(0, c = r.value), "as_item" in r && o(10, p = r.as_item), "visible" in r && o(11, v = r.visible), "elem_id" in r && o(12, K = r.elem_id), "elem_classes" in r && o(13, S = r.elem_classes), "elem_style" in r && o(14, P = r.elem_style), "$$scope" in r && o(18, a = r.$$scope);
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
      visible: v,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: p,
      value: c
    });
  }, [c, i, s, u, m, I, E, f, d, b, p, v, K, S, P, n, l, M, a];
}
class xe extends oe {
  constructor(e) {
    super(), be(this, e, Se, Ke, pe, {
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
    }), h();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), h();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), h();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), h();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), h();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), h();
  }
}
export {
  xe as I,
  Pe as g,
  g as w
};
