async function F() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function V(t) {
  return await F(), t().then((e) => e.default);
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
      const c = l[1], r = c.split("_"), _ = (...f) => {
        const p = f.map((u) => f && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
        return e.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let f = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = f;
        for (let u = 1; u < r.length - 1; u++) {
          const h = {
            ...n.props[r[u]] || {}
          };
          f[r[u]] = h, f = h;
        }
        const p = r[r.length - 1];
        return f[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, i;
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
  function i(c) {
    if (Z(t, c) && (t = c, o)) {
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
  function s(c) {
    i(c(t));
  }
  function l(c, r = P) {
    const _ = [c, r];
    return n.add(_), n.size === 1 && (o = e(i, s) || P), c(t), () => {
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
  setContext: I
} = window.__gradio__svelte__internal, G = "$$ms-gr-antd-slots-key";
function H() {
  const t = g({});
  return I(G, t);
}
const J = "$$ms-gr-antd-context-key";
function Q(t) {
  var c;
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
  const n = x(J), i = ((c = y(n)) == null ? void 0 : c.as_item) || t.as_item, s = n ? i ? y(n)[i] : y(n) : {}, l = g({
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
const L = "$$ms-gr-antd-slot-key";
function T() {
  I(L, g(void 0));
}
function W() {
  return x(L);
}
const M = "$$ms-gr-antd-component-slot-context-key";
function $({
  slot: t,
  index: e,
  subIndex: o
}) {
  return I(M, {
    slotKey: g(t),
    slotIndex: g(e),
    subSlotIndex: g(o)
  });
}
function Se() {
  return x(M);
}
function ee(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var R = {
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
        var c = arguments[l];
        c && (s = i(s, n(c)));
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
      for (var c in s)
        e.call(s, c) && s[c] && (l = i(l, c));
      return l;
    }
    function i(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    t.exports ? (o.default = o, t.exports = o) : window.classNames = o;
  })();
})(R);
var te = R.exports;
const O = /* @__PURE__ */ ee(te), {
  SvelteComponent: ne,
  assign: se,
  check_outros: ie,
  component_subscribe: j,
  create_component: oe,
  create_slot: le,
  destroy_component: re,
  detach: U,
  empty: X,
  flush: b,
  get_all_dirty_from_scope: ce,
  get_slot_changes: ue,
  get_spread_object: q,
  get_spread_update: ae,
  group_outros: _e,
  handle_promise: fe,
  init: me,
  insert: Y,
  mount_component: de,
  noop: m,
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
    /*AwaitedListItemMeta*/
    t[2],
    n
  ), {
    c() {
      e = X(), n.block.c();
    },
    m(i, s) {
      Y(i, e, s), n.block.m(i, n.anchor = s), n.mount = () => e.parentNode, n.anchor = e, o = !0;
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
      i && U(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function ge(t) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
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
        "ms-gr-antd-list-item-meta"
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
  return e = new /*ListItemMeta*/
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
      const c = l & /*$mergedProps, $slots*/
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
          "ms-gr-antd-list-item-meta"
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
      65536 && (c.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(c);
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
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ce(t) {
  let e, o, n = (
    /*$mergedProps*/
    t[0].visible && A(t)
  );
  return {
    c() {
      n && n.c(), e = X();
    },
    m(i, s) {
      n && n.m(i, s), Y(i, e, s), o = !0;
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
      i && U(e), n && n.d(i);
    }
  };
}
function Ke(t, e, o) {
  let n, i, s, {
    $$slots: l = {},
    $$scope: c
  } = e;
  const r = V(() => import("./list.item.meta-DnITzjqn.js"));
  let {
    gradio: _
  } = e, {
    _internal: d = {}
  } = e, {
    as_item: f
  } = e, {
    props: p = {}
  } = e;
  const u = g(p);
  j(t, u, (a) => o(14, n = a));
  let {
    elem_id: h = ""
  } = e, {
    elem_classes: K = []
  } = e, {
    elem_style: S = {}
  } = e, {
    visible: v = !0
  } = e;
  const [N, D] = Q({
    gradio: _,
    props: n,
    _internal: d,
    as_item: f,
    visible: v,
    elem_id: h,
    elem_classes: K,
    elem_style: S
  });
  j(t, N, (a) => o(0, i = a));
  const z = H();
  return j(t, z, (a) => o(1, s = a)), t.$$set = (a) => {
    "gradio" in a && o(6, _ = a.gradio), "_internal" in a && o(7, d = a._internal), "as_item" in a && o(8, f = a.as_item), "props" in a && o(9, p = a.props), "elem_id" in a && o(10, h = a.elem_id), "elem_classes" in a && o(11, K = a.elem_classes), "elem_style" in a && o(12, S = a.elem_style), "visible" in a && o(13, v = a.visible), "$$scope" in a && o(16, c = a.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && u.update((a) => ({
      ...a,
      ...p
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, as_item, visible, elem_id, elem_classes, elem_style*/
    32192 && D({
      gradio: _,
      props: n,
      _internal: d,
      as_item: f,
      visible: v,
      elem_id: h,
      elem_classes: K,
      elem_style: S
    });
  }, [i, s, r, u, N, z, _, d, f, p, h, K, S, v, n, l, c];
}
class ve extends ne {
  constructor(e) {
    super(), me(this, e, Ke, Ce, pe, {
      gradio: 6,
      _internal: 7,
      as_item: 8,
      props: 9,
      elem_id: 10,
      elem_classes: 11,
      elem_style: 12,
      visible: 13
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
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[10];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[11];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[12];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
}
export {
  ve as I,
  Se as g,
  g as w
};
