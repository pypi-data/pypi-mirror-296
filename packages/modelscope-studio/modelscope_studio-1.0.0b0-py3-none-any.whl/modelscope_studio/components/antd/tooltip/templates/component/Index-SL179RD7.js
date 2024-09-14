async function T() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(t) {
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
      const a = l[1], c = a.split("_"), f = (...m) => {
        const p = m.map((u) => m && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
          payload: p,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        o[c[0]] = m;
        for (let u = 1; u < c.length - 1; u++) {
          const h = {
            ...n.props[c[u]] || {}
          };
          m[c[u]] = h, m = h;
        }
        const p = c[c.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, o;
      }
      const d = c[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function j() {
}
function Z(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function B(t, ...e) {
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
  return B(t, (i) => e = i)(), e;
}
const w = [];
function g(t, e = j) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(a) {
    if (Z(t, a) && (t = a, i)) {
      const c = !w.length;
      for (const f of n)
        f[1](), w.push(f, t);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function s(a) {
    o(a(t));
  }
  function l(a, c = j) {
    const f = [a, c];
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
} = window.__gradio__svelte__internal, G = "$$ms-gr-antd-slots-key";
function H() {
  const t = g({});
  return I(G, t);
}
const J = "$$ms-gr-antd-context-key";
function Q(t) {
  var a;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = $(), i = ee({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), W();
  const n = z(J), o = ((a = y(n)) == null ? void 0 : a.as_item) || t.as_item, s = n ? o ? y(n)[o] : y(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((d) => ({
      ...d,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(n)[c.as_item] : y(n);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function W() {
  I(U, g(void 0));
}
function $() {
  return z(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function ee({
  slot: t,
  index: e,
  subIndex: i
}) {
  return I(X, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(i)
  });
}
function ve() {
  return z(X);
}
function te(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var Y = {
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
})(Y);
var ne = Y.exports;
const x = /* @__PURE__ */ te(ne), {
  SvelteComponent: se,
  assign: ie,
  check_outros: oe,
  component_subscribe: N,
  create_component: le,
  create_slot: re,
  destroy_component: ce,
  detach: D,
  empty: F,
  flush: b,
  get_all_dirty_from_scope: ue,
  get_slot_changes: ae,
  get_spread_object: A,
  get_spread_update: fe,
  group_outros: _e,
  handle_promise: me,
  init: de,
  insert: L,
  mount_component: pe,
  noop: _,
  safe_not_equal: be,
  transition_in: k,
  transition_out: C,
  update_await_block_branch: he,
  update_slot_base: ge
} = window.__gradio__svelte__internal;
function R(t) {
  let e, i, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ce,
    then: we,
    catch: ye,
    value: 19,
    blocks: [, , ,]
  };
  return me(
    /*AwaitedTooltip*/
    t[2],
    n
  ), {
    c() {
      e = F(), n.block.c();
    },
    m(o, s) {
      L(o, e, s), n.block.m(o, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, i = !0;
    },
    p(o, s) {
      t = o, he(n, t, s);
    },
    i(o) {
      i || (k(n.block), i = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        C(l);
      }
      i = !1;
    },
    d(o) {
      o && D(e), n.block.d(o), n.token = null, n = null;
    }
  };
}
function ye(t) {
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
        t[0].elem_style
      )
    },
    {
      className: x(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-tooltip"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    /*$mergedProps*/
    t[0].props,
    q(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    },
    {
      title: (
        /*$mergedProps*/
        t[0].props.title || /*$mergedProps*/
        t[0].title
      )
    }
  ];
  let o = {
    $$slots: {
      default: [ke]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    o = ie(o, n[s]);
  return e = new /*Tooltip*/
  t[19]({
    props: o
  }), {
    c() {
      le(e.$$.fragment);
    },
    m(s, l) {
      pe(e, s, l), i = !0;
    },
    p(s, l) {
      const a = l & /*$mergedProps, $slots*/
      3 ? fe(n, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: x(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-tooltip"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && A(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && A(q(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }, l & /*$mergedProps*/
      1 && {
        title: (
          /*$mergedProps*/
          s[0].props.title || /*$mergedProps*/
          s[0].title
        )
      }]) : {};
      l & /*$$scope*/
      131072 && (a.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      i || (k(e.$$.fragment, s), i = !0);
    },
    o(s) {
      C(e.$$.fragment, s), i = !1;
    },
    d(s) {
      ce(e, s);
    }
  };
}
function ke(t) {
  let e;
  const i = (
    /*#slots*/
    t[16].default
  ), n = re(
    i,
    t,
    /*$$scope*/
    t[17],
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
      131072) && ge(
        n,
        i,
        o,
        /*$$scope*/
        o[17],
        e ? ae(
          i,
          /*$$scope*/
          o[17],
          s,
          null
        ) : ue(
          /*$$scope*/
          o[17]
        ),
        null
      );
    },
    i(o) {
      e || (k(n, o), e = !0);
    },
    o(o) {
      C(n, o), e = !1;
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
    t[0].visible && R(t)
  );
  return {
    c() {
      n && n.c(), e = F();
    },
    m(o, s) {
      n && n.m(o, s), L(o, e, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && k(n, 1)) : (n = R(o), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (_e(), C(n, 1, 1, () => {
        n = null;
      }), oe());
    },
    i(o) {
      i || (k(n), i = !0);
    },
    o(o) {
      C(n), i = !1;
    },
    d(o) {
      o && D(e), n && n.d(o);
    }
  };
}
function Se(t, e, i) {
  let n, o, s, {
    $$slots: l = {},
    $$scope: a
  } = e;
  const c = V(() => import("./tooltip-mm8e0RNp.js"));
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
    title: u = ""
  } = e, {
    as_item: h
  } = e, {
    visible: K = !0
  } = e, {
    elem_id: S = ""
  } = e, {
    elem_classes: v = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [E, M] = Q({
    gradio: f,
    props: n,
    _internal: p,
    visible: K,
    elem_id: S,
    elem_classes: v,
    elem_style: P,
    as_item: h,
    title: u
  });
  N(t, E, (r) => i(0, o = r));
  const O = H();
  return N(t, O, (r) => i(1, s = r)), t.$$set = (r) => {
    "gradio" in r && i(6, f = r.gradio), "props" in r && i(7, d = r.props), "_internal" in r && i(8, p = r._internal), "title" in r && i(9, u = r.title), "as_item" in r && i(10, h = r.as_item), "visible" in r && i(11, K = r.visible), "elem_id" in r && i(12, S = r.elem_id), "elem_classes" in r && i(13, v = r.elem_classes), "elem_style" in r && i(14, P = r.elem_style), "$$scope" in r && i(17, a = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && m.update((r) => ({
      ...r,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, title*/
    65344 && M({
      gradio: f,
      props: n,
      _internal: p,
      visible: K,
      elem_id: S,
      elem_classes: v,
      elem_style: P,
      as_item: h,
      title: u
    });
  }, [o, s, c, m, E, O, f, d, p, u, h, K, S, v, P, n, l, a];
}
class Pe extends se {
  constructor(e) {
    super(), de(this, e, Se, Ke, be, {
      gradio: 6,
      props: 7,
      _internal: 8,
      title: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), b();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get title() {
    return this.$$.ctx[9];
  }
  set title(e) {
    this.$$set({
      title: e
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
  Pe as I,
  ve as g,
  g as w
};
