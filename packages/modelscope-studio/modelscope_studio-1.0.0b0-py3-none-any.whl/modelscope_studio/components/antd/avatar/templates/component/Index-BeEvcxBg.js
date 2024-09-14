async function V() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function Z(t) {
  return await V(), t().then((e) => e.default);
}
function q(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
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
        return e.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: n
        });
      };
      if (c.length > 1) {
        let m = {
          ...n.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const h = {
            ...n.props[c[a]] || {}
          };
          m[c[a]] = h, m = h;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const d = c[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return i;
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
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return G(t, (o) => e = o)(), e;
}
const w = [];
function g(t, e = j) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(u) {
    if (B(t, u) && (t = u, o)) {
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
  function s(u) {
    i(u(t));
  }
  function l(u, c = j) {
    const f = [u, c];
    return n.add(f), n.size === 1 && (o = e(i, s) || j), u(t), () => {
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
  getContext: z,
  setContext: I
} = window.__gradio__svelte__internal, H = "$$ms-gr-antd-slots-key";
function J() {
  const t = g({});
  return I(H, t);
}
const Q = "$$ms-gr-antd-context-key";
function T(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = $(), o = ee({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    o.slotKey.set(c);
  }), W();
  const n = z(Q), i = ((u = y(n)) == null ? void 0 : u.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = g({
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
  subIndex: o
}) {
  return I(X, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function Se() {
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
    function o() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (s = i(s, n(u)));
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
      for (var u in s)
        e.call(s, u) && s[u] && (l = i(l, u));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(Y);
var ne = Y.exports;
const x = /* @__PURE__ */ te(ne), {
  SvelteComponent: se,
  assign: oe,
  check_outros: ie,
  component_subscribe: N,
  create_component: le,
  create_slot: re,
  destroy_component: ce,
  detach: D,
  empty: F,
  flush: p,
  get_all_dirty_from_scope: ae,
  get_slot_changes: ue,
  get_spread_object: A,
  get_spread_update: fe,
  group_outros: _e,
  handle_promise: me,
  init: de,
  insert: L,
  mount_component: be,
  noop: _,
  safe_not_equal: pe,
  transition_in: k,
  transition_out: v,
  update_await_block_branch: he,
  update_slot_base: ge
} = window.__gradio__svelte__internal;
function R(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ve,
    then: we,
    catch: ye,
    value: 19,
    blocks: [, , ,]
  };
  return me(
    /*AwaitedAvatar*/
    t[2],
    n
  ), {
    c() {
      e = F(), n.block.c();
    },
    m(i, s) {
      L(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, he(n, t, s);
    },
    i(i) {
      o || (k(n.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const l = n.blocks[s];
        v(l);
      }
      o = !1;
    },
    d(i) {
      i && D(e), n.block.d(i), n.token = null, n = null;
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
  let e, o;
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
        "ms-gr-antd-avatar"
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
      src: (
        /*$mergedProps*/
        t[0].props.src || /*$mergedProps*/
        t[0].src
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ke]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = oe(i, n[s]);
  return e = new /*Avatar*/
  t[19]({
    props: i
  }), {
    c() {
      le(e.$$.fragment);
    },
    m(s, l) {
      be(e, s, l), o = !0;
    },
    p(s, l) {
      const u = l & /*$mergedProps, $slots*/
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
          "ms-gr-antd-avatar"
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
        src: (
          /*$mergedProps*/
          s[0].props.src || /*$mergedProps*/
          s[0].src
        )
      }]) : {};
      l & /*$$scope*/
      131072 && (u.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(u);
    },
    i(s) {
      o || (k(e.$$.fragment, s), o = !0);
    },
    o(s) {
      v(e.$$.fragment, s), o = !1;
    },
    d(s) {
      ce(e, s);
    }
  };
}
function ke(t) {
  let e;
  const o = (
    /*#slots*/
    t[16].default
  ), n = re(
    o,
    t,
    /*$$scope*/
    t[17],
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
      131072) && ge(
        n,
        o,
        i,
        /*$$scope*/
        i[17],
        e ? ue(
          o,
          /*$$scope*/
          i[17],
          s,
          null
        ) : ae(
          /*$$scope*/
          i[17]
        ),
        null
      );
    },
    i(i) {
      e || (k(n, i), e = !0);
    },
    o(i) {
      v(n, i), e = !1;
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
function Ce(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && R(t)
  );
  return {
    c() {
      n && n.c(), e = F();
    },
    m(i, s) {
      n && n.m(i, s), L(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && k(n, 1)) : (n = R(i), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (_e(), v(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(i) {
      o || (k(n), o = !0);
    },
    o(i) {
      v(n), o = !1;
    },
    d(i) {
      i && D(e), n && n.d(i);
    }
  };
}
function Ke(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: u
  } = e;
  const c = Z(() => import("./avatar-DtIjAIIS.js"));
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
    src: a = ""
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
  const [E, M] = T({
    gradio: f,
    props: n,
    _internal: b,
    src: a,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: h
  });
  N(t, E, (r) => o(0, i = r));
  const O = J();
  return N(t, O, (r) => o(1, s = r)), t.$$set = (r) => {
    "gradio" in r && o(6, f = r.gradio), "props" in r && o(7, d = r.props), "_internal" in r && o(8, b = r._internal), "src" in r && o(9, a = r.src), "as_item" in r && o(10, h = r.as_item), "visible" in r && o(11, C = r.visible), "elem_id" in r && o(12, K = r.elem_id), "elem_classes" in r && o(13, S = r.elem_classes), "elem_style" in r && o(14, P = r.elem_style), "$$scope" in r && o(17, u = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && m.update((r) => ({
      ...r,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, src, visible, elem_id, elem_classes, elem_style, as_item*/
    65344 && M({
      gradio: f,
      props: n,
      _internal: b,
      src: a,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: h
    });
  }, [i, s, c, m, E, O, f, d, b, a, h, C, K, S, P, n, l, u];
}
class Pe extends se {
  constructor(e) {
    super(), de(this, e, Ke, Ce, pe, {
      gradio: 6,
      props: 7,
      _internal: 8,
      src: 9,
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
    }), p();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get src() {
    return this.$$.ctx[9];
  }
  set src(e) {
    this.$$set({
      src: e
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
  Pe as I,
  Se as g,
  g as w
};
