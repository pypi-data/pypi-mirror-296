async function B() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function G(e) {
  return await B(), e().then((t) => t.default);
}
function F(e) {
  const {
    gradio: t,
    _internal: o,
    ...s
  } = e;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const r = l[1], c = r.split("_"), f = (...m) => {
        const p = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return t.dispatch(r.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        i[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const g = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = g, m = g;
        }
        const p = c[c.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, i;
      }
      const _ = c[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function N() {
}
function H(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function J(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return N;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return J(e, (o) => t = o)(), t;
}
const w = [];
function h(e, t = N) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(r) {
    if (H(e, r) && (e = r, o)) {
      const c = !w.length;
      for (const f of s)
        f[1](), w.push(f, e);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(r) {
    i(r(e));
  }
  function l(r, c = N) {
    const f = [r, c];
    return s.add(f), s.size === 1 && (o = t(i, n) || N), r(e), () => {
      s.delete(f), s.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: n,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: x
} = window.__gradio__svelte__internal, Q = "$$ms-gr-antd-slots-key";
function W() {
  const e = h({});
  return x(Q, e);
}
const $ = "$$ms-gr-antd-context-key";
function ee(e) {
  var r;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ne(), o = se({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    o.slotKey.set(c);
  }), te();
  const s = z($), i = ((r = y(s)) == null ? void 0 : r.as_item) || e.as_item, n = s ? i ? y(s)[i] : y(s) : {}, l = h({
    ...e,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: f
    } = y(l);
    f && (c = c[f]), l.update((_) => ({
      ..._,
      ...c
    }));
  }), [l, (c) => {
    const f = c.as_item ? y(s)[c.as_item] : y(s);
    return l.set({
      ...c,
      ...f
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function te() {
  x(U, h(void 0));
}
function ne() {
  return z(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: e,
  index: t,
  subIndex: o
}) {
  return x(X, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(o)
  });
}
function Ee() {
  return z(X);
}
function ie(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Y = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function o() {
      for (var n = "", l = 0; l < arguments.length; l++) {
        var r = arguments[l];
        r && (n = i(n, s(r)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return o.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var l = "";
      for (var r in n)
        t.call(n, r) && n[r] && (l = i(l, r));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(Y);
var oe = Y.exports;
const M = /* @__PURE__ */ ie(oe), {
  getContext: le,
  setContext: re
} = window.__gradio__svelte__internal;
function ce(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(i = ["default"]) {
    const n = i.reduce((l, r) => (l[r] = h([]), l), {});
    return re(t, {
      itemsMap: n,
      allowedSlots: i
    }), n;
  }
  function s() {
    const {
      itemsMap: i,
      allowedSlots: n
    } = le(t);
    return function(l, r, c) {
      i && (l ? i[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[r] = c : _[r] = void 0, _;
      }) : n.includes("default") && i.default.update((f) => {
        const _ = [...f];
        return _[r] = c, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: s
  };
}
const {
  getItems: ue,
  getSetItemFn: Oe
} = ce("timeline"), {
  SvelteComponent: ae,
  assign: fe,
  check_outros: _e,
  component_subscribe: k,
  create_component: me,
  create_slot: de,
  destroy_component: pe,
  detach: D,
  empty: L,
  flush: b,
  get_all_dirty_from_scope: be,
  get_slot_changes: he,
  get_spread_object: V,
  get_spread_update: ge,
  group_outros: ye,
  handle_promise: we,
  init: Ce,
  insert: T,
  mount_component: ke,
  noop: d,
  safe_not_equal: Se,
  transition_in: C,
  transition_out: S,
  update_await_block_branch: Ke,
  update_slot_base: Ie
} = window.__gradio__svelte__internal;
function R(e) {
  let t, o, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ne,
    then: Pe,
    catch: ve,
    value: 22,
    blocks: [, , ,]
  };
  return we(
    /*AwaitedTimeline*/
    e[4],
    s
  ), {
    c() {
      t = L(), s.block.c();
    },
    m(i, n) {
      T(i, t, n), s.block.m(i, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, o = !0;
    },
    p(i, n) {
      e = i, Ke(s, e, n);
    },
    i(i) {
      o || (C(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        S(l);
      }
      o = !1;
    },
    d(i) {
      i && D(t), s.block.d(i), s.token = null, s = null;
    }
  };
}
function ve(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Pe(e) {
  let t, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: M(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-timeline"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    F(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      slotItems: (
        /*$items*/
        e[2].length > 0 ? (
          /*$items*/
          e[2]
        ) : (
          /*$children*/
          e[3]
        )
      )
    }
  ];
  let i = {
    $$slots: {
      default: [je]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    i = fe(i, s[n]);
  return t = new /*Timeline*/
  e[22]({
    props: i
  }), {
    c() {
      me(t.$$.fragment);
    },
    m(n, l) {
      ke(t, n, l), o = !0;
    },
    p(n, l) {
      const r = l & /*$mergedProps, $slots, $items, $children*/
      15 ? ge(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: M(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-timeline"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && V(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && V(F(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$items, $children*/
      12 && {
        slotItems: (
          /*$items*/
          n[2].length > 0 ? (
            /*$items*/
            n[2]
          ) : (
            /*$children*/
            n[3]
          )
        )
      }]) : {};
      l & /*$$scope*/
      1048576 && (r.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(r);
    },
    i(n) {
      o || (C(t.$$.fragment, n), o = !0);
    },
    o(n) {
      S(t.$$.fragment, n), o = !1;
    },
    d(n) {
      pe(t, n);
    }
  };
}
function je(e) {
  let t;
  const o = (
    /*#slots*/
    e[19].default
  ), s = de(
    o,
    e,
    /*$$scope*/
    e[20],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(i, n) {
      s && s.m(i, n), t = !0;
    },
    p(i, n) {
      s && s.p && (!t || n & /*$$scope*/
      1048576) && Ie(
        s,
        o,
        i,
        /*$$scope*/
        i[20],
        t ? he(
          o,
          /*$$scope*/
          i[20],
          n,
          null
        ) : be(
          /*$$scope*/
          i[20]
        ),
        null
      );
    },
    i(i) {
      t || (C(s, i), t = !0);
    },
    o(i) {
      S(s, i), t = !1;
    },
    d(i) {
      s && s.d(i);
    }
  };
}
function Ne(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function ze(e) {
  let t, o, s = (
    /*$mergedProps*/
    e[0].visible && R(e)
  );
  return {
    c() {
      s && s.c(), t = L();
    },
    m(i, n) {
      s && s.m(i, n), T(i, t, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[0].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = R(i), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (ye(), S(s, 1, 1, () => {
        s = null;
      }), _e());
    },
    i(i) {
      o || (C(s), o = !0);
    },
    o(i) {
      S(s), o = !1;
    },
    d(i) {
      i && D(t), s && s.d(i);
    }
  };
}
function xe(e, t, o) {
  let s, i, n, l, r, {
    $$slots: c = {},
    $$scope: f
  } = t;
  const _ = G(() => import("./timeline-B5twh01Z.js"));
  let {
    gradio: m
  } = t, {
    props: p = {}
  } = t;
  const a = h(p);
  k(e, a, (u) => o(18, s = u));
  let {
    _internal: g = {}
  } = t, {
    as_item: K
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: v = ""
  } = t, {
    elem_classes: P = []
  } = t, {
    elem_style: j = {}
  } = t;
  const [E, Z] = ee({
    gradio: m,
    props: s,
    _internal: g,
    visible: I,
    elem_id: v,
    elem_classes: P,
    elem_style: j,
    as_item: K
  });
  k(e, E, (u) => o(0, i = u));
  const O = W();
  k(e, O, (u) => o(1, n = u));
  const {
    items: q,
    default: A
  } = ue(["items", "default"]);
  return k(e, q, (u) => o(2, l = u)), k(e, A, (u) => o(3, r = u)), e.$$set = (u) => {
    "gradio" in u && o(10, m = u.gradio), "props" in u && o(11, p = u.props), "_internal" in u && o(12, g = u._internal), "as_item" in u && o(13, K = u.as_item), "visible" in u && o(14, I = u.visible), "elem_id" in u && o(15, v = u.elem_id), "elem_classes" in u && o(16, P = u.elem_classes), "elem_style" in u && o(17, j = u.elem_style), "$$scope" in u && o(20, f = u.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    2048 && a.update((u) => ({
      ...u,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item*/
    521216 && Z({
      gradio: m,
      props: s,
      _internal: g,
      visible: I,
      elem_id: v,
      elem_classes: P,
      elem_style: j,
      as_item: K
    });
  }, [i, n, l, r, _, a, E, O, q, A, m, p, g, K, I, v, P, j, s, c, f];
}
class qe extends ae {
  constructor(t) {
    super(), Ce(this, t, xe, ze, Se, {
      gradio: 10,
      props: 11,
      _internal: 12,
      as_item: 13,
      visible: 14,
      elem_id: 15,
      elem_classes: 16,
      elem_style: 17
    });
  }
  get gradio() {
    return this.$$.ctx[10];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[11];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[12];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[13];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[14];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[15];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[16];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[17];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  qe as I,
  Ee as g,
  h as w
};
