async function M() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(t) {
  return await M(), t().then((e) => e.default);
}
function E(t) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = t;
  return Object.keys(o).reduce((i, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], r = u.split("_"), _ = (...m) => {
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
        return e.dispatch(u.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let m = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = m;
        for (let c = 1; c < r.length - 1; c++) {
          const h = {
            ...n.props[r[c]] || {}
          };
          m[r[c]] = h, m = h;
        }
        const p = r[r.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, i;
      }
      const d = r[0];
      i[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return i;
  }, {});
}
function P() {
}
function Z(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function B(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return P;
  }
  const o = t.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(t) {
  let e;
  return B(t, (o) => e = o)(), e;
}
const w = [];
function g(t, e = P) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(u) {
    if (Z(t, u) && (t = u, o)) {
      const r = !w.length;
      for (const _ of n)
        _[1](), w.push(_, t);
      if (r) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function s(u) {
    i(u(t));
  }
  function l(u, r = P) {
    const _ = [u, r];
    return n.add(_), n.size === 1 && (o = e(i, s) || P), u(t), () => {
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
  getContext: x,
  setContext: N
} = window.__gradio__svelte__internal, G = "$$ms-gr-antd-slots-key";
function H() {
  const t = g({});
  return N(G, t);
}
const J = "$$ms-gr-antd-context-key";
function Q(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = W(), o = $({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), T();
  const n = x(J), i = ((u = y(n)) == null ? void 0 : u.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = g({
    ...t,
    ...s
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: _
    } = y(l);
    _ && (r = r[_]), l.update((d) => ({
      ...d,
      ...r
    }));
  }), [l, (r) => {
    const _ = r.as_item ? y(n)[r.as_item] : y(n);
    return l.set({
      ...r,
      ..._
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const R = "$$ms-gr-antd-slot-key";
function T() {
  N(R, g(void 0));
}
function W() {
  return x(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: t,
  index: e,
  subIndex: o
}) {
  return N(U, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function Ke() {
  return x(U);
}
function ee(t) {
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
})(X);
var te = X.exports;
const O = /* @__PURE__ */ ee(te), {
  SvelteComponent: ne,
  assign: se,
  check_outros: ie,
  component_subscribe: j,
  create_component: oe,
  create_slot: le,
  destroy_component: re,
  detach: Y,
  empty: D,
  flush: b,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  get_spread_object: q,
  get_spread_update: ae,
  group_outros: _e,
  handle_promise: fe,
  init: me,
  insert: F,
  mount_component: de,
  noop: f,
  safe_not_equal: pe,
  transition_in: k,
  transition_out: C,
  update_await_block_branch: be,
  update_slot_base: he
} = window.__gradio__svelte__internal;
function A(t) {
  let e, o, n = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ke,
    then: ye,
    catch: ge,
    value: 18,
    blocks: [, , ,]
  };
  return fe(
    /*AwaitedSpin*/
    t[2],
    n
  ), {
    c() {
      e = D(), n.block.c();
    },
    m(i, s) {
      F(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, s) {
      t = i, be(n, t, s);
    },
    i(i) {
      o || (k(n.block), o = !0);
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
function ge(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function ye(t) {
  let e, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: O(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-spin"
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
    E(
      /*$mergedProps*/
      t[0]
    ),
    {
      slots: (
        /*$slots*/
        t[1]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [we]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    i = se(i, n[s]);
  return e = new /*Spin*/
  t[18]({
    props: i
  }), {
    c() {
      oe(e.$$.fragment);
    },
    m(s, l) {
      de(e, s, l), o = !0;
    },
    p(s, l) {
      const u = l & /*$mergedProps, $slots*/
      3 ? ae(n, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: O(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-spin"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && q(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && q(E(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }]) : {};
      l & /*$$scope*/
      65536 && (u.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(u);
    },
    i(s) {
      o || (k(e.$$.fragment, s), o = !0);
    },
    o(s) {
      C(e.$$.fragment, s), o = !1;
    },
    d(s) {
      re(e, s);
    }
  };
}
function we(t) {
  let e;
  const o = (
    /*#slots*/
    t[15].default
  ), n = le(
    o,
    t,
    /*$$scope*/
    t[16],
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
      65536) && he(
        n,
        o,
        i,
        /*$$scope*/
        i[16],
        e ? ue(
          o,
          /*$$scope*/
          i[16],
          s,
          null
        ) : ce(
          /*$$scope*/
          i[16]
        ),
        null
      );
    },
    i(i) {
      e || (k(n, i), e = !0);
    },
    o(i) {
      C(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function ke(t) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ce(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && A(t)
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
      i[0].visible ? n ? (n.p(i, s), s & /*$mergedProps*/
      1 && k(n, 1)) : (n = A(i), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (_e(), C(n, 1, 1, () => {
        n = null;
      }), ie());
    },
    i(i) {
      o || (k(n), o = !0);
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
    $$scope: u
  } = e;
  const r = V(() => import("./spin-BdzhxKOm.js"));
  let {
    gradio: _
  } = e, {
    props: d = {}
  } = e;
  const m = g(d);
  j(t, m, (a) => o(14, n = a));
  let {
    _internal: p = {}
  } = e, {
    as_item: c
  } = e, {
    visible: h = !0
  } = e, {
    elem_id: S = ""
  } = e, {
    elem_classes: K = []
  } = e, {
    elem_style: v = {}
  } = e;
  const [z, L] = Q({
    gradio: _,
    props: n,
    _internal: p,
    visible: h,
    elem_id: S,
    elem_classes: K,
    elem_style: v,
    as_item: c
  });
  j(t, z, (a) => o(0, i = a));
  const I = H();
  return j(t, I, (a) => o(1, s = a)), t.$$set = (a) => {
    "gradio" in a && o(6, _ = a.gradio), "props" in a && o(7, d = a.props), "_internal" in a && o(8, p = a._internal), "as_item" in a && o(9, c = a.as_item), "visible" in a && o(10, h = a.visible), "elem_id" in a && o(11, S = a.elem_id), "elem_classes" in a && o(12, K = a.elem_classes), "elem_style" in a && o(13, v = a.elem_style), "$$scope" in a && o(16, u = a.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && m.update((a) => ({
      ...a,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    32576 && L({
      gradio: _,
      props: n,
      _internal: p,
      visible: h,
      elem_id: S,
      elem_classes: K,
      elem_style: v,
      as_item: c
    });
  }, [i, s, r, m, z, I, _, d, p, c, h, S, K, v, n, l, u];
}
class ve extends ne {
  constructor(e) {
    super(), me(this, e, Se, Ce, pe, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      visible: 10,
      elem_id: 11,
      elem_classes: 12,
      elem_style: 13
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
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[10];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[11];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[12];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[13];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  ve as I,
  Ke as g,
  g as w
};
