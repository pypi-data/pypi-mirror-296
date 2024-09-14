async function H() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function J(e) {
  return await H(), e().then((t) => t.default);
}
function M(e) {
  const {
    gradio: t,
    _internal: o,
    ...s
  } = e;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const r = l[1], u = r.split("_"), f = (...m) => {
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
      if (u.length > 1) {
        let m = {
          ...s.props[u[0]] || {}
        };
        i[u[0]] = m;
        for (let a = 1; a < u.length - 1; a++) {
          const g = {
            ...s.props[u[a]] || {}
          };
          m[u[a]] = g, m = g;
        }
        const p = u[u.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, i;
      }
      const _ = u[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function z() {
}
function Q(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function T(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return z;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return T(e, (o) => t = o)(), t;
}
const w = [];
function h(e, t = z) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(r) {
    if (Q(e, r) && (e = r, o)) {
      const u = !w.length;
      for (const f of s)
        f[1](), w.push(f, e);
      if (u) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(r) {
    i(r(e));
  }
  function l(r, u = z) {
    const f = [r, u];
    return s.add(f), s.size === 1 && (o = t(i, n) || z), r(e), () => {
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
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, W = "$$ms-gr-antd-slots-key";
function $() {
  const e = h({});
  return O(W, e);
}
const ee = "$$ms-gr-antd-context-key";
function te(e) {
  var r;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = se(), o = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((u) => {
    o.slotKey.set(u);
  }), ne();
  const s = E(ee), i = ((r = y(s)) == null ? void 0 : r.as_item) || e.as_item, n = s ? i ? y(s)[i] : y(s) : {}, l = h({
    ...e,
    ...n
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: f
    } = y(l);
    f && (u = u[f]), l.update((_) => ({
      ..._,
      ...u
    }));
  }), [l, (u) => {
    const f = u.as_item ? y(s)[u.as_item] : y(s);
    return l.set({
      ...u,
      ...f
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function ne() {
  O(U, h(void 0));
}
function se() {
  return E(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: e,
  index: t,
  subIndex: o
}) {
  return O(X, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(o)
  });
}
function qe() {
  return E(X);
}
function oe(e) {
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
var le = Y.exports;
const V = /* @__PURE__ */ oe(le), {
  getContext: re,
  setContext: ce
} = window.__gradio__svelte__internal;
function ue(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(i = ["default"]) {
    const n = i.reduce((l, r) => (l[r] = h([]), l), {});
    return ce(t, {
      itemsMap: n,
      allowedSlots: i
    }), n;
  }
  function s() {
    const {
      itemsMap: i,
      allowedSlots: n
    } = re(t);
    return function(l, r, u) {
      i && (l ? i[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[r] = u : _[r] = void 0, _;
      }) : n.includes("default") && i.default.update((f) => {
        const _ = [...f];
        return _[r] = u, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: s
  };
}
const {
  getItems: ae,
  getSetItemFn: Ae
} = ue("descriptions"), {
  SvelteComponent: fe,
  assign: _e,
  check_outros: me,
  component_subscribe: k,
  create_component: de,
  create_slot: pe,
  destroy_component: be,
  detach: L,
  empty: Z,
  flush: b,
  get_all_dirty_from_scope: he,
  get_slot_changes: ge,
  get_spread_object: D,
  get_spread_update: ye,
  group_outros: we,
  handle_promise: Ce,
  init: ke,
  insert: B,
  mount_component: Se,
  noop: d,
  safe_not_equal: Ke,
  transition_in: C,
  transition_out: S,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function R(e) {
  let t, o, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: ze,
    then: je,
    catch: ve,
    value: 23,
    blocks: [, , ,]
  };
  return Ce(
    /*AwaitedDescriptions*/
    e[4],
    s
  ), {
    c() {
      t = Z(), s.block.c();
    },
    m(i, n) {
      B(i, t, n), s.block.m(i, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, o = !0;
    },
    p(i, n) {
      e = i, Ie(s, e, n);
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
      i && L(t), s.block.d(i), s.token = null, s = null;
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
function je(e) {
  let t, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: V(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-descriptions"
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
    M(
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
      title: (
        /*$mergedProps*/
        e[0].props.title || /*$mergedProps*/
        e[0].title
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
      default: [Ne]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    i = _e(i, s[n]);
  return t = new /*Descriptions*/
  e[23]({
    props: i
  }), {
    c() {
      de(t.$$.fragment);
    },
    m(n, l) {
      Se(t, n, l), o = !0;
    },
    p(n, l) {
      const r = l & /*$mergedProps, $slots, $items, $children*/
      15 ? ye(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: V(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-descriptions"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && D(
        /*$mergedProps*/
        n[0].props
      ), l & /*$mergedProps*/
      1 && D(M(
        /*$mergedProps*/
        n[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$mergedProps*/
      1 && {
        title: (
          /*$mergedProps*/
          n[0].props.title || /*$mergedProps*/
          n[0].title
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
      2097152 && (r.$$scope = {
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
      be(t, n);
    }
  };
}
function Ne(e) {
  let t;
  const o = (
    /*#slots*/
    e[20].default
  ), s = pe(
    o,
    e,
    /*$$scope*/
    e[21],
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
      2097152) && Pe(
        s,
        o,
        i,
        /*$$scope*/
        i[21],
        t ? ge(
          o,
          /*$$scope*/
          i[21],
          n,
          null
        ) : he(
          /*$$scope*/
          i[21]
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
function ze(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Ee(e) {
  let t, o, s = (
    /*$mergedProps*/
    e[0].visible && R(e)
  );
  return {
    c() {
      s && s.c(), t = Z();
    },
    m(i, n) {
      s && s.m(i, n), B(i, t, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[0].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = R(i), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (we(), S(s, 1, 1, () => {
        s = null;
      }), me());
    },
    i(i) {
      o || (C(s), o = !0);
    },
    o(i) {
      S(s), o = !1;
    },
    d(i) {
      i && L(t), s && s.d(i);
    }
  };
}
function Oe(e, t, o) {
  let s, i, n, l, r, {
    $$slots: u = {},
    $$scope: f
  } = t;
  const _ = J(() => import("./descriptions-B7EPQz6A.js"));
  let {
    gradio: m
  } = t, {
    props: p = {}
  } = t;
  const a = h(p);
  k(e, a, (c) => o(19, s = c));
  let {
    _internal: g = {}
  } = t, {
    title: K
  } = t, {
    as_item: I
  } = t, {
    visible: P = !0
  } = t, {
    elem_id: v = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: N = {}
  } = t;
  const [q, G] = te({
    gradio: m,
    props: s,
    _internal: g,
    visible: P,
    elem_id: v,
    elem_classes: j,
    elem_style: N,
    as_item: I,
    title: K
  });
  k(e, q, (c) => o(0, i = c));
  const A = $();
  k(e, A, (c) => o(1, n = c));
  const {
    items: x,
    default: F
  } = ae(["default", "items"]);
  return k(e, x, (c) => o(2, l = c)), k(e, F, (c) => o(3, r = c)), e.$$set = (c) => {
    "gradio" in c && o(10, m = c.gradio), "props" in c && o(11, p = c.props), "_internal" in c && o(12, g = c._internal), "title" in c && o(13, K = c.title), "as_item" in c && o(14, I = c.as_item), "visible" in c && o(15, P = c.visible), "elem_id" in c && o(16, v = c.elem_id), "elem_classes" in c && o(17, j = c.elem_classes), "elem_style" in c && o(18, N = c.elem_style), "$$scope" in c && o(21, f = c.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    2048 && a.update((c) => ({
      ...c,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, title*/
    1045504 && G({
      gradio: m,
      props: s,
      _internal: g,
      visible: P,
      elem_id: v,
      elem_classes: j,
      elem_style: N,
      as_item: I,
      title: K
    });
  }, [i, n, l, r, _, a, q, A, x, F, m, p, g, K, I, P, v, j, N, s, u, f];
}
class xe extends fe {
  constructor(t) {
    super(), ke(this, t, Oe, Ee, Ke, {
      gradio: 10,
      props: 11,
      _internal: 12,
      title: 13,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
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
  get title() {
    return this.$$.ctx[13];
  }
  set title(t) {
    this.$$set({
      title: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[15];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[16];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[17];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[18];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  xe as I,
  qe as g,
  h as w
};
