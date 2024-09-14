async function B() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function G(t) {
  return await B(), t().then((e) => e.default);
}
function A(t) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = t;
  return Object.keys(i).reduce((o, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const r = l[1], c = r.split("_"), _ = (...f) => {
        const b = f.map((a) => f && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return e.dispatch(r.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let f = {
          ...s.props[c[0]] || {}
        };
        o[c[0]] = f;
        for (let a = 1; a < c.length - 1; a++) {
          const g = {
            ...s.props[c[a]] || {}
          };
          f[c[a]] = g, f = g;
        }
        const b = c[c.length - 1];
        return f[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = _, o;
      }
      const m = c[0];
      o[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function j() {
}
function H(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function J(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return j;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return J(t, (i) => e = i)(), e;
}
const w = [];
function h(t, e = j) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(r) {
    if (H(t, r) && (t = r, i)) {
      const c = !w.length;
      for (const _ of s)
        _[1](), w.push(_, t);
      if (c) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function n(r) {
    o(r(t));
  }
  function l(r, c = j) {
    const _ = [r, c];
    return s.add(_), s.size === 1 && (i = e(o, n) || j), r(t), () => {
      s.delete(_), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
  };
}
const {
  getContext: N,
  setContext: z
} = window.__gradio__svelte__internal, Q = "$$ms-gr-antd-slots-key";
function T() {
  const t = h({});
  return z(Q, t);
}
const W = "$$ms-gr-antd-context-key";
function $(t) {
  var r;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = te(), i = ne({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), ee();
  const s = N(W), o = ((r = y(s)) == null ? void 0 : r.as_item) || t.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...t,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: _
    } = y(l);
    _ && (c = c[_]), l.update((m) => ({
      ...m,
      ...c
    }));
  }), [l, (c) => {
    const _ = c.as_item ? y(s)[c.as_item] : y(s);
    return l.set({
      ...c,
      ..._
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const D = "$$ms-gr-antd-slot-key";
function ee() {
  z(D, h(void 0));
}
function te() {
  return N(D);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function ne({
  slot: t,
  index: e,
  subIndex: i
}) {
  return z(R, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function ze() {
  return N(R);
}
function se(t) {
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
        var r = arguments[l];
        r && (n = o(n, s(r)));
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
      for (var r in n)
        e.call(n, r) && n[r] && (l = o(l, r));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(U);
var oe = U.exports;
const F = /* @__PURE__ */ se(oe), {
  getContext: ie,
  setContext: le
} = window.__gradio__svelte__internal;
function re(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((l, r) => (l[r] = h([]), l), {});
    return le(e, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = ie(e);
    return function(l, r, c) {
      o && (l ? o[l].update((_) => {
        const m = [..._];
        return n.includes(l) ? m[r] = c : m[r] = void 0, m;
      }) : n.includes("default") && o.default.update((_) => {
        const m = [..._];
        return m[r] = c, m;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: s
  };
}
const {
  getItems: ce,
  getSetItemFn: Ee
} = re("menu"), {
  SvelteComponent: ue,
  assign: ae,
  check_outros: _e,
  component_subscribe: x,
  create_component: me,
  create_slot: fe,
  destroy_component: de,
  detach: X,
  empty: Y,
  flush: p,
  get_all_dirty_from_scope: pe,
  get_slot_changes: be,
  get_spread_object: M,
  get_spread_update: he,
  group_outros: ge,
  handle_promise: ye,
  init: we,
  insert: L,
  mount_component: Ce,
  noop: d,
  safe_not_equal: ke,
  transition_in: C,
  transition_out: k,
  update_await_block_branch: Se,
  update_slot_base: Ke
} = window.__gradio__svelte__internal;
function V(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: xe,
    then: ve,
    catch: Ie,
    value: 21,
    blocks: [, , ,]
  };
  return ye(
    /*AwaitedDropdown*/
    t[3],
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
      i || (C(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        k(l);
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
function ve(t) {
  let e, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: F(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-dropdown"
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
    A(
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
      menuItems: (
        /*$items*/
        t[2]
      )
    },
    {
      innerStyle: (
        /*$mergedProps*/
        t[0].inner_elem_style
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Pe]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = ae(o, s[n]);
  return e = new /*Dropdown*/
  t[21]({
    props: o
  }), {
    c() {
      me(e.$$.fragment);
    },
    m(n, l) {
      Ce(e, n, l), i = !0;
    },
    p(n, l) {
      const r = l & /*$mergedProps, $slots, $items*/
      7 ? he(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: F(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-dropdown"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && M(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && M(A(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$items*/
      4 && {
        menuItems: (
          /*$items*/
          n[2]
        )
      }, l & /*$mergedProps*/
      1 && {
        innerStyle: (
          /*$mergedProps*/
          n[0].inner_elem_style
        )
      }]) : {};
      l & /*$$scope*/
      524288 && (r.$$scope = {
        dirty: l,
        ctx: n
      }), e.$set(r);
    },
    i(n) {
      i || (C(e.$$.fragment, n), i = !0);
    },
    o(n) {
      k(e.$$.fragment, n), i = !1;
    },
    d(n) {
      de(e, n);
    }
  };
}
function Pe(t) {
  let e;
  const i = (
    /*#slots*/
    t[18].default
  ), s = fe(
    i,
    t,
    /*$$scope*/
    t[19],
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
      524288) && Ke(
        s,
        i,
        o,
        /*$$scope*/
        o[19],
        e ? be(
          i,
          /*$$scope*/
          o[19],
          n,
          null
        ) : pe(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      e || (C(s, o), e = !0);
    },
    o(o) {
      k(s, o), e = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function xe(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function je(t) {
  let e, i, s = (
    /*$mergedProps*/
    t[0].visible && V(t)
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
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = V(o), s.c(), C(s, 1), s.m(e.parentNode, e)) : s && (ge(), k(s, 1, 1, () => {
        s = null;
      }), _e());
    },
    i(o) {
      i || (C(s), i = !0);
    },
    o(o) {
      k(s), i = !1;
    },
    d(o) {
      o && X(e), s && s.d(o);
    }
  };
}
function Ne(t, e, i) {
  let s, o, n, l, {
    $$slots: r = {},
    $$scope: c
  } = e;
  const _ = G(() => import("./dropdown-DIyJU8V8.js"));
  let {
    gradio: m
  } = e, {
    props: f = {}
  } = e;
  const b = h(f);
  x(t, b, (u) => i(17, s = u));
  let {
    _internal: a = {}
  } = e, {
    as_item: g
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: v = {}
  } = e, {
    inner_elem_style: P = {}
  } = e;
  const [E, Z] = $({
    gradio: m,
    props: s,
    _internal: a,
    visible: S,
    elem_id: K,
    elem_classes: I,
    elem_style: v,
    as_item: g,
    inner_elem_style: P
  });
  x(t, E, (u) => i(0, o = u));
  const O = T();
  x(t, O, (u) => i(1, n = u));
  const {
    "menu.items": q
  } = ce(["menu.items"]);
  return x(t, q, (u) => i(2, l = u)), t.$$set = (u) => {
    "gradio" in u && i(8, m = u.gradio), "props" in u && i(9, f = u.props), "_internal" in u && i(10, a = u._internal), "as_item" in u && i(11, g = u.as_item), "visible" in u && i(12, S = u.visible), "elem_id" in u && i(13, K = u.elem_id), "elem_classes" in u && i(14, I = u.elem_classes), "elem_style" in u && i(15, v = u.elem_style), "inner_elem_style" in u && i(16, P = u.inner_elem_style), "$$scope" in u && i(19, c = u.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && b.update((u) => ({
      ...u,
      ...f
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, inner_elem_style*/
    261376 && Z({
      gradio: m,
      props: s,
      _internal: a,
      visible: S,
      elem_id: K,
      elem_classes: I,
      elem_style: v,
      as_item: g,
      inner_elem_style: P
    });
  }, [o, n, l, _, b, E, O, q, m, f, a, g, S, K, I, v, P, s, r, c];
}
class Oe extends ue {
  constructor(e) {
    super(), we(this, e, Ne, je, ke, {
      gradio: 8,
      props: 9,
      _internal: 10,
      as_item: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15,
      inner_elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), p();
  }
  get props() {
    return this.$$.ctx[9];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[11];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
  get inner_elem_style() {
    return this.$$.ctx[16];
  }
  set inner_elem_style(e) {
    this.$$set({
      inner_elem_style: e
    }), p();
  }
}
export {
  Oe as I,
  ze as g,
  h as w
};
