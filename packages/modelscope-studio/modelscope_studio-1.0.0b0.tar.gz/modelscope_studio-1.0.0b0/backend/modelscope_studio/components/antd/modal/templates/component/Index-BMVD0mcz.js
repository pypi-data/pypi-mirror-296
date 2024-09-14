async function L() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(t) {
  return await L(), t().then((e) => e.default);
}
function E(t) {
  const {
    gradio: e,
    _internal: i,
    ...n
  } = t;
  return Object.keys(i).reduce((o, s) => {
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
        o[r[0]] = m;
        for (let c = 1; c < r.length - 1; c++) {
          const h = {
            ...n.props[r[c]] || {}
          };
          m[r[c]] = h, m = h;
        }
        const p = r[r.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, o;
      }
      const d = r[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return o;
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
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return B(t, (i) => e = i)(), e;
}
const w = [];
function g(t, e = P) {
  let i;
  const n = /* @__PURE__ */ new Set();
  function o(u) {
    if (Z(t, u) && (t = u, i)) {
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
    o(u(t));
  }
  function l(u, r = P) {
    const _ = [u, r];
    return n.add(_), n.size === 1 && (i = e(o, s) || P), u(t), () => {
      n.delete(_), n.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
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
  const e = W(), i = $({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((r) => {
    i.slotKey.set(r);
  }), T();
  const n = x(J), o = ((u = y(n)) == null ? void 0 : u.as_item) || t.as_item, s = n ? o ? y(n)[o] : y(n) : {}, l = g({
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
const M = "$$ms-gr-antd-slot-key";
function T() {
  N(M, g(void 0));
}
function W() {
  return x(M);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: t,
  index: e,
  subIndex: i
}) {
  return N(R, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(i)
  });
}
function Se() {
  return x(R);
}
function ee(t) {
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
      for (var s = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (s = o(s, n(u)));
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
      for (var u in s)
        e.call(s, u) && s[u] && (l = o(l, u));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(U);
var te = U.exports;
const O = /* @__PURE__ */ ee(te), {
  SvelteComponent: ne,
  assign: se,
  check_outros: oe,
  component_subscribe: j,
  create_component: ie,
  create_slot: le,
  destroy_component: re,
  detach: X,
  empty: Y,
  flush: b,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  get_spread_object: q,
  get_spread_update: ae,
  group_outros: _e,
  handle_promise: fe,
  init: me,
  insert: D,
  mount_component: de,
  noop: f,
  safe_not_equal: pe,
  transition_in: k,
  transition_out: C,
  update_await_block_branch: be,
  update_slot_base: he
} = window.__gradio__svelte__internal;
function A(t) {
  let e, i, n = {
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
    /*AwaitedModal*/
    t[2],
    n
  ), {
    c() {
      e = Y(), n.block.c();
    },
    m(o, s) {
      D(o, e, s), n.block.m(o, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, i = !0;
    },
    p(o, s) {
      t = o, be(n, t, s);
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
      o && X(e), n.block.d(o), n.token = null, n = null;
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
  let e, i;
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
        "ms-gr-antd-modal"
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
  let o = {
    $$slots: {
      default: [we]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let s = 0; s < n.length; s += 1)
    o = se(o, n[s]);
  return e = new /*Modal*/
  t[18]({
    props: o
  }), {
    c() {
      ie(e.$$.fragment);
    },
    m(s, l) {
      de(e, s, l), i = !0;
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
          "ms-gr-antd-modal"
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
      i || (k(e.$$.fragment, s), i = !0);
    },
    o(s) {
      C(e.$$.fragment, s), i = !1;
    },
    d(s) {
      re(e, s);
    }
  };
}
function we(t) {
  let e;
  const i = (
    /*#slots*/
    t[15].default
  ), n = le(
    i,
    t,
    /*$$scope*/
    t[16],
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
      65536) && he(
        n,
        i,
        o,
        /*$$scope*/
        o[16],
        e ? ue(
          i,
          /*$$scope*/
          o[16],
          s,
          null
        ) : ce(
          /*$$scope*/
          o[16]
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
  let e, i, n = (
    /*$mergedProps*/
    t[0].visible && A(t)
  );
  return {
    c() {
      n && n.c(), e = Y();
    },
    m(o, s) {
      n && n.m(o, s), D(o, e, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? n ? (n.p(o, s), s & /*$mergedProps*/
      1 && k(n, 1)) : (n = A(o), n.c(), k(n, 1), n.m(e.parentNode, e)) : n && (_e(), C(n, 1, 1, () => {
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
      o && X(e), n && n.d(o);
    }
  };
}
function Ke(t, e, i) {
  let n, o, s, {
    $$slots: l = {},
    $$scope: u
  } = e;
  const r = V(() => import("./modal-DFsTbGp4.js"));
  let {
    gradio: _
  } = e, {
    props: d = {}
  } = e;
  const m = g(d);
  j(t, m, (a) => i(14, n = a));
  let {
    _internal: p = {}
  } = e, {
    as_item: c
  } = e, {
    visible: h = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: v = {}
  } = e;
  const [z, F] = Q({
    gradio: _,
    props: n,
    _internal: p,
    visible: h,
    elem_id: K,
    elem_classes: S,
    elem_style: v,
    as_item: c
  });
  j(t, z, (a) => i(0, o = a));
  const I = H();
  return j(t, I, (a) => i(1, s = a)), t.$$set = (a) => {
    "gradio" in a && i(6, _ = a.gradio), "props" in a && i(7, d = a.props), "_internal" in a && i(8, p = a._internal), "as_item" in a && i(9, c = a.as_item), "visible" in a && i(10, h = a.visible), "elem_id" in a && i(11, K = a.elem_id), "elem_classes" in a && i(12, S = a.elem_classes), "elem_style" in a && i(13, v = a.elem_style), "$$scope" in a && i(16, u = a.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    128 && m.update((a) => ({
      ...a,
      ...d
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    32576 && F({
      gradio: _,
      props: n,
      _internal: p,
      visible: h,
      elem_id: K,
      elem_classes: S,
      elem_style: v,
      as_item: c
    });
  }, [o, s, r, m, z, I, _, d, p, c, h, K, S, v, n, l, u];
}
class ve extends ne {
  constructor(e) {
    super(), me(this, e, Ke, Ce, pe, {
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
  Se as g,
  g as w
};
