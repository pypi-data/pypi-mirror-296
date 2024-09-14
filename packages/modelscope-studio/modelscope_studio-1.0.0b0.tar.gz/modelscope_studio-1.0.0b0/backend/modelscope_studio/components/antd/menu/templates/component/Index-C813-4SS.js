async function T() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function W(e) {
  return await T(), e().then((t) => t.default);
}
function F(e) {
  const {
    gradio: t,
    _internal: o,
    ...n
  } = e;
  return Object.keys(o).reduce((s, i) => {
    const u = i.match(/bind_(.+)_event/);
    if (u) {
      const l = u[1], r = l.split("_"), a = (...m) => {
        const p = m.map((f) => m && typeof f == "object" && (f.nativeEvent || f instanceof Event) ? {
          type: f.type,
          detail: f.detail,
          timestamp: f.timeStamp,
          clientX: f.clientX,
          clientY: f.clientY,
          targetId: f.target.id,
          targetClassName: f.target.className,
          altKey: f.altKey,
          ctrlKey: f.ctrlKey,
          shiftKey: f.shiftKey,
          metaKey: f.metaKey
        } : f);
        return t.dispatch(l.replace(/[A-Z]/g, (f) => "_" + f.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let m = {
          ...n.props[r[0]] || {}
        };
        s[r[0]] = m;
        for (let f = 1; f < r.length - 1; f++) {
          const g = {
            ...n.props[r[f]] || {}
          };
          m[r[f]] = g, m = g;
        }
        const p = r[r.length - 1];
        return m[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = a, s;
      }
      const _ = r[0];
      s[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = a;
    }
    return s;
  }, {});
}
function z() {
}
function x(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function $(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return z;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return $(e, (o) => t = o)(), t;
}
const w = [];
function h(e, t = z) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function s(l) {
    if (x(e, l) && (e = l, o)) {
      const r = !w.length;
      for (const a of n)
        a[1](), w.push(a, e);
      if (r) {
        for (let a = 0; a < w.length; a += 2)
          w[a][0](w[a + 1]);
        w.length = 0;
      }
    }
  }
  function i(l) {
    s(l(e));
  }
  function u(l, r = z) {
    const a = [l, r];
    return n.add(a), n.size === 1 && (o = t(s, i) || z), l(e), () => {
      n.delete(a), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: s,
    update: i,
    subscribe: u
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, ee = "$$ms-gr-antd-slots-key";
function te() {
  const e = h({});
  return O(ee, e);
}
const ne = "$$ms-gr-antd-context-key";
function se(e) {
  var l;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ie(), o = le({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    o.slotKey.set(r);
  }), oe();
  const n = E(ne), s = ((l = y(n)) == null ? void 0 : l.as_item) || e.as_item, i = n ? s ? y(n)[s] : y(n) : {}, u = h({
    ...e,
    ...i
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: a
    } = y(u);
    a && (r = r[a]), u.update((_) => ({
      ..._,
      ...r
    }));
  }), [u, (r) => {
    const a = r.as_item ? y(n)[r.as_item] : y(n);
    return u.set({
      ...r,
      ...a
    });
  }]) : [u, (r) => {
    u.set(r);
  }];
}
const Y = "$$ms-gr-antd-slot-key";
function oe() {
  O(Y, h(void 0));
}
function ie() {
  return E(Y);
}
const D = "$$ms-gr-antd-component-slot-context-key";
function le({
  slot: e,
  index: t,
  subIndex: o
}) {
  return O(D, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(o)
  });
}
function Ae() {
  return E(D);
}
function re(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var L = {
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
      for (var i = "", u = 0; u < arguments.length; u++) {
        var l = arguments[u];
        l && (i = s(i, n(l)));
      }
      return i;
    }
    function n(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return o.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var u = "";
      for (var l in i)
        t.call(i, l) && i[l] && (u = s(u, l));
      return u;
    }
    function s(i, u) {
      return u ? i ? i + " " + u : i + u : i;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(L);
var ue = L.exports;
const R = /* @__PURE__ */ re(ue), {
  getContext: ce,
  setContext: ae
} = window.__gradio__svelte__internal;
function fe(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(s = ["default"]) {
    const i = s.reduce((u, l) => (u[l] = h([]), u), {});
    return ae(t, {
      itemsMap: i,
      allowedSlots: s
    }), i;
  }
  function n() {
    const {
      itemsMap: s,
      allowedSlots: i
    } = ce(t);
    return function(u, l, r) {
      s && (u ? s[u].update((a) => {
        const _ = [...a];
        return i.includes(u) ? _[l] = r : _[l] = void 0, _;
      }) : i.includes("default") && s.default.update((a) => {
        const _ = [...a];
        return _[l] = r, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: n
  };
}
const {
  getItems: _e,
  getSetItemFn: Me
} = fe("menu"), {
  SvelteComponent: me,
  assign: de,
  check_outros: pe,
  component_subscribe: K,
  create_component: be,
  create_slot: he,
  destroy_component: ge,
  detach: Z,
  empty: B,
  flush: b,
  get_all_dirty_from_scope: ye,
  get_slot_changes: we,
  get_spread_object: U,
  get_spread_update: ke,
  group_outros: Ce,
  handle_promise: Ke,
  init: ve,
  insert: G,
  mount_component: Se,
  noop: d,
  safe_not_equal: Ie,
  transition_in: k,
  transition_out: v,
  update_await_block_branch: Pe,
  update_slot_base: je
} = window.__gradio__svelte__internal;
function X(e) {
  let t, o, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Oe,
    then: ze,
    catch: Ne,
    value: 24,
    blocks: [, , ,]
  };
  return Ke(
    /*AwaitedMenu*/
    e[5],
    n
  ), {
    c() {
      t = B(), n.block.c();
    },
    m(s, i) {
      G(s, t, i), n.block.m(s, n.anchor = i), n.mount = () => t.parentNode, n.anchor = t, o = !0;
    },
    p(s, i) {
      e = s, Pe(n, e, i);
    },
    i(s) {
      o || (k(n.block), o = !0);
    },
    o(s) {
      for (let i = 0; i < 3; i += 1) {
        const u = n.blocks[i];
        v(u);
      }
      o = !1;
    },
    d(s) {
      s && Z(t), n.block.d(s), n.token = null, n = null;
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
  var i, u;
  let t, o;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: R(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-menu"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[1].elem_id
      )
    },
    /*$mergedProps*/
    e[1].props,
    F(
      /*$mergedProps*/
      e[1]
    ),
    {
      slots: (
        /*$slots*/
        e[2]
      )
    },
    {
      slotItems: (
        /*$items*/
        e[3].length > 0 ? (
          /*$items*/
          e[3]
        ) : (
          /*$children*/
          e[4]
        )
      )
    },
    {
      openKeys: (
        /*$mergedProps*/
        e[1].props.openKeys || /*$mergedProps*/
        ((i = e[1].value) == null ? void 0 : i.open_keys) || void 0
      )
    },
    {
      selectedKeys: (
        /*$mergedProps*/
        e[1].props.selectedKeys || /*$mergedProps*/
        ((u = e[1].value) == null ? void 0 : u.selected_keys) || void 0
      )
    },
    {
      onValueChange: (
        /*func*/
        e[21]
      )
    }
  ];
  let s = {
    $$slots: {
      default: [Ee]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let l = 0; l < n.length; l += 1)
    s = de(s, n[l]);
  return t = new /*Menu*/
  e[24]({
    props: s
  }), {
    c() {
      be(t.$$.fragment);
    },
    m(l, r) {
      Se(t, l, r), o = !0;
    },
    p(l, r) {
      var _, m;
      const a = r & /*$mergedProps, $slots, $items, $children, undefined, value*/
      31 ? ke(n, [r & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          l[1].elem_style
        )
      }, r & /*$mergedProps*/
      2 && {
        className: R(
          /*$mergedProps*/
          l[1].elem_classes,
          "ms-gr-antd-menu"
        )
      }, r & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          l[1].elem_id
        )
      }, r & /*$mergedProps*/
      2 && U(
        /*$mergedProps*/
        l[1].props
      ), r & /*$mergedProps*/
      2 && U(F(
        /*$mergedProps*/
        l[1]
      )), r & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          l[2]
        )
      }, r & /*$items, $children*/
      24 && {
        slotItems: (
          /*$items*/
          l[3].length > 0 ? (
            /*$items*/
            l[3]
          ) : (
            /*$children*/
            l[4]
          )
        )
      }, r & /*$mergedProps, undefined*/
      2 && {
        openKeys: (
          /*$mergedProps*/
          l[1].props.openKeys || /*$mergedProps*/
          ((_ = l[1].value) == null ? void 0 : _.open_keys) || void 0
        )
      }, r & /*$mergedProps, undefined*/
      2 && {
        selectedKeys: (
          /*$mergedProps*/
          l[1].props.selectedKeys || /*$mergedProps*/
          ((m = l[1].value) == null ? void 0 : m.selected_keys) || void 0
        )
      }, r & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          l[21]
        )
      }]) : {};
      r & /*$$scope*/
      4194304 && (a.$$scope = {
        dirty: r,
        ctx: l
      }), t.$set(a);
    },
    i(l) {
      o || (k(t.$$.fragment, l), o = !0);
    },
    o(l) {
      v(t.$$.fragment, l), o = !1;
    },
    d(l) {
      ge(t, l);
    }
  };
}
function Ee(e) {
  let t;
  const o = (
    /*#slots*/
    e[20].default
  ), n = he(
    o,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(s, i) {
      n && n.m(s, i), t = !0;
    },
    p(s, i) {
      n && n.p && (!t || i & /*$$scope*/
      4194304) && je(
        n,
        o,
        s,
        /*$$scope*/
        s[22],
        t ? we(
          o,
          /*$$scope*/
          s[22],
          i,
          null
        ) : ye(
          /*$$scope*/
          s[22]
        ),
        null
      );
    },
    i(s) {
      t || (k(n, s), t = !0);
    },
    o(s) {
      v(n, s), t = !1;
    },
    d(s) {
      n && n.d(s);
    }
  };
}
function Oe(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function qe(e) {
  let t, o, n = (
    /*$mergedProps*/
    e[1].visible && X(e)
  );
  return {
    c() {
      n && n.c(), t = B();
    },
    m(s, i) {
      n && n.m(s, i), G(s, t, i), o = !0;
    },
    p(s, [i]) {
      /*$mergedProps*/
      s[1].visible ? n ? (n.p(s, i), i & /*$mergedProps*/
      2 && k(n, 1)) : (n = X(s), n.c(), k(n, 1), n.m(t.parentNode, t)) : n && (Ce(), v(n, 1, 1, () => {
        n = null;
      }), pe());
    },
    i(s) {
      o || (k(n), o = !0);
    },
    o(s) {
      v(n), o = !1;
    },
    d(s) {
      s && Z(t), n && n.d(s);
    }
  };
}
function Ve(e, t, o) {
  let n, s, i, u, l, {
    $$slots: r = {},
    $$scope: a
  } = t;
  const _ = W(() => import("./menu-DvxHvdOa.js"));
  let {
    gradio: m
  } = t, {
    props: p = {}
  } = t;
  const f = h(p);
  K(e, f, (c) => o(19, n = c));
  let {
    _internal: g = {}
  } = t, {
    value: C = {}
  } = t, {
    as_item: S
  } = t, {
    visible: I = !0
  } = t, {
    elem_id: P = ""
  } = t, {
    elem_classes: j = []
  } = t, {
    elem_style: N = {}
  } = t;
  const [q, H] = se({
    gradio: m,
    props: n,
    _internal: g,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: S,
    value: C
  });
  K(e, q, (c) => o(1, s = c));
  const V = te();
  K(e, V, (c) => o(2, i = c));
  const {
    items: A,
    default: M
  } = _e(["default", "items"]);
  K(e, A, (c) => o(3, u = c)), K(e, M, (c) => o(4, l = c));
  const J = ({
    openKeys: c,
    selectedKeys: Q
  }) => {
    o(0, C = {
      open_keys: c,
      selected_keys: Q
    });
  };
  return e.$$set = (c) => {
    "gradio" in c && o(11, m = c.gradio), "props" in c && o(12, p = c.props), "_internal" in c && o(13, g = c._internal), "value" in c && o(0, C = c.value), "as_item" in c && o(14, S = c.as_item), "visible" in c && o(15, I = c.visible), "elem_id" in c && o(16, P = c.elem_id), "elem_classes" in c && o(17, j = c.elem_classes), "elem_style" in c && o(18, N = c.elem_style), "$$scope" in c && o(22, a = c.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    4096 && f.update((c) => ({
      ...c,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    1042433 && H({
      gradio: m,
      props: n,
      _internal: g,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: S,
      value: C
    });
  }, [C, s, i, u, l, _, f, q, V, A, M, m, p, g, S, I, P, j, N, n, r, J, a];
}
class Fe extends me {
  constructor(t) {
    super(), ve(this, t, Ve, qe, Ie, {
      gradio: 11,
      props: 12,
      _internal: 13,
      value: 0,
      as_item: 14,
      visible: 15,
      elem_id: 16,
      elem_classes: 17,
      elem_style: 18
    });
  }
  get gradio() {
    return this.$$.ctx[11];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[12];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
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
  Fe as I,
  Ae as g,
  h as w
};
