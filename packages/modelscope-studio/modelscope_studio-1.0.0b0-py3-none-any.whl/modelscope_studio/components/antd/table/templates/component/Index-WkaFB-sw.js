async function Q() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function W(e) {
  return await Q(), e().then((t) => t.default);
}
function U(e) {
  const {
    gradio: t,
    _internal: l,
    ...s
  } = e;
  return Object.keys(l).reduce((o, n) => {
    const i = n.match(/bind_(.+)_event/);
    if (i) {
      const c = i[1], a = c.split("_"), m = (...d) => {
        const b = d.map((u) => d && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
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
        return t.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (a.length > 1) {
        let d = {
          ...s.props[a[0]] || {}
        };
        o[a[0]] = d;
        for (let u = 1; u < a.length - 1; u++) {
          const h = {
            ...s.props[a[u]] || {}
          };
          d[a[u]] = h, d = h;
        }
        const b = a[a.length - 1];
        return d[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = m, o;
      }
      const _ = a[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = m;
    }
    return o;
  }, {});
}
function E() {
}
function $(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function ee(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return E;
  }
  const l = e.subscribe(...t);
  return l.unsubscribe ? () => l.unsubscribe() : l;
}
function w(e) {
  let t;
  return ee(e, (l) => t = l)(), t;
}
const y = [];
function g(e, t = E) {
  let l;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if ($(e, c) && (e = c, l)) {
      const a = !y.length;
      for (const m of s)
        m[1](), y.push(m, e);
      if (a) {
        for (let m = 0; m < y.length; m += 2)
          y[m][0](y[m + 1]);
        y.length = 0;
      }
    }
  }
  function n(c) {
    o(c(e));
  }
  function i(c, a = E) {
    const m = [c, a];
    return s.add(m), s.size === 1 && (l = t(o, n) || E), c(e), () => {
      s.delete(m), s.size === 0 && l && (l(), l = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: i
  };
}
const {
  getContext: N,
  setContext: z
} = window.__gradio__svelte__internal, te = "$$ms-gr-antd-slots-key";
function ne() {
  const e = g({});
  return z(te, e);
}
const se = "$$ms-gr-antd-context-key";
function oe(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ie(), l = re({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((a) => {
    l.slotKey.set(a);
  }), le();
  const s = N(se), o = ((c = w(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? w(s)[o] : w(s) : {}, i = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((a) => {
    const {
      as_item: m
    } = w(i);
    m && (a = a[m]), i.update((_) => ({
      ..._,
      ...a
    }));
  }), [i, (a) => {
    const m = a.as_item ? w(s)[a.as_item] : w(s);
    return i.set({
      ...a,
      ...m
    });
  }]) : [i, (a) => {
    i.set(a);
  }];
}
const L = "$$ms-gr-antd-slot-key";
function le() {
  z(L, g(void 0));
}
function ie() {
  return N(L);
}
const T = "$$ms-gr-antd-component-slot-context-key";
function re({
  slot: e,
  index: t,
  subIndex: l
}) {
  return z(T, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(l)
  });
}
function Re() {
  return N(T);
}
function ce(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var Z = {
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
    function l() {
      for (var n = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (n = o(n, s(c)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return l.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var i = "";
      for (var c in n)
        t.call(n, c) && n[c] && (i = o(i, c));
      return i;
    }
    function o(n, i) {
      return i ? n ? n + " " + i : n + i : n;
    }
    e.exports ? (l.default = l, e.exports = l) : window.classNames = l;
  })();
})(Z);
var ae = Z.exports;
const X = /* @__PURE__ */ ce(ae), {
  getContext: ue,
  setContext: me
} = window.__gradio__svelte__internal;
function O(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function l(o = ["default"]) {
    const n = o.reduce((i, c) => (i[c] = g([]), i), {});
    return me(t, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = ue(t);
    return function(i, c, a) {
      o && (i ? o[i].update((m) => {
        const _ = [...m];
        return n.includes(i) ? _[c] = a : _[c] = void 0, _;
      }) : n.includes("default") && o.default.update((m) => {
        const _ = [...m];
        return _[c] = a, _;
      }));
    };
  }
  return {
    getItems: l,
    getSetItemFn: s
  };
}
const {
  getItems: _e,
  getSetItemFn: Me
} = O("table-column"), {
  getItems: fe,
  getSetItemFn: Ve
} = O("table-row-selection"), {
  getItems: de,
  getSetItemFn: Ue
} = O("table-expandable"), {
  SvelteComponent: be,
  assign: pe,
  check_outros: ge,
  component_subscribe: S,
  create_component: he,
  create_slot: we,
  destroy_component: ye,
  detach: B,
  empty: G,
  flush: p,
  get_all_dirty_from_scope: Se,
  get_slot_changes: Ie,
  get_spread_object: Y,
  get_spread_update: Ce,
  group_outros: ke,
  handle_promise: Ke,
  init: xe,
  insert: H,
  mount_component: Pe,
  noop: f,
  safe_not_equal: ve,
  transition_in: I,
  transition_out: C,
  update_await_block_branch: je,
  update_slot_base: Ee
} = window.__gradio__svelte__internal;
function D(e) {
  let t, l, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Oe,
    then: Ne,
    catch: Fe,
    value: 25,
    blocks: [, , ,]
  };
  return Ke(
    /*AwaitedTable*/
    e[5],
    s
  ), {
    c() {
      t = G(), s.block.c();
    },
    m(o, n) {
      H(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, l = !0;
    },
    p(o, n) {
      e = o, je(s, e, n);
    },
    i(o) {
      l || (I(s.block), l = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const i = s.blocks[n];
        C(i);
      }
      l = !1;
    },
    d(o) {
      o && B(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function Fe(e) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ne(e) {
  let t, l;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: X(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-table"
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
    U(
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
      dataSource: (
        /*$mergedProps*/
        e[0].props.dataSource ?? /*$mergedProps*/
        e[0].data_source
      )
    },
    {
      rowSelectionItems: (
        /*$rowSelectionItems*/
        e[2]
      )
    },
    {
      expandableItems: (
        /*$expandableItems*/
        e[3]
      )
    },
    {
      columnItems: (
        /*$columnItems*/
        e[4]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [ze]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = pe(o, s[n]);
  return t = new /*Table*/
  e[25]({
    props: o
  }), {
    c() {
      he(t.$$.fragment);
    },
    m(n, i) {
      Pe(t, n, i), l = !0;
    },
    p(n, i) {
      const c = i & /*$mergedProps, $slots, $rowSelectionItems, $expandableItems, $columnItems*/
      31 ? Ce(s, [i & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, i & /*$mergedProps*/
      1 && {
        className: X(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-table"
        )
      }, i & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, i & /*$mergedProps*/
      1 && Y(
        /*$mergedProps*/
        n[0].props
      ), i & /*$mergedProps*/
      1 && Y(U(
        /*$mergedProps*/
        n[0]
      )), i & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, i & /*$mergedProps*/
      1 && {
        dataSource: (
          /*$mergedProps*/
          n[0].props.dataSource ?? /*$mergedProps*/
          n[0].data_source
        )
      }, i & /*$rowSelectionItems*/
      4 && {
        rowSelectionItems: (
          /*$rowSelectionItems*/
          n[2]
        )
      }, i & /*$expandableItems*/
      8 && {
        expandableItems: (
          /*$expandableItems*/
          n[3]
        )
      }, i & /*$columnItems*/
      16 && {
        columnItems: (
          /*$columnItems*/
          n[4]
        )
      }]) : {};
      i & /*$$scope*/
      8388608 && (c.$$scope = {
        dirty: i,
        ctx: n
      }), t.$set(c);
    },
    i(n) {
      l || (I(t.$$.fragment, n), l = !0);
    },
    o(n) {
      C(t.$$.fragment, n), l = !1;
    },
    d(n) {
      ye(t, n);
    }
  };
}
function ze(e) {
  let t;
  const l = (
    /*#slots*/
    e[22].default
  ), s = we(
    l,
    e,
    /*$$scope*/
    e[23],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, n) {
      s && s.m(o, n), t = !0;
    },
    p(o, n) {
      s && s.p && (!t || n & /*$$scope*/
      8388608) && Ee(
        s,
        l,
        o,
        /*$$scope*/
        o[23],
        t ? Ie(
          l,
          /*$$scope*/
          o[23],
          n,
          null
        ) : Se(
          /*$$scope*/
          o[23]
        ),
        null
      );
    },
    i(o) {
      t || (I(s, o), t = !0);
    },
    o(o) {
      C(s, o), t = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Oe(e) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function qe(e) {
  let t, l, s = (
    /*$mergedProps*/
    e[0].visible && D(e)
  );
  return {
    c() {
      s && s.c(), t = G();
    },
    m(o, n) {
      s && s.m(o, n), H(o, t, n), l = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && I(s, 1)) : (s = D(o), s.c(), I(s, 1), s.m(t.parentNode, t)) : s && (ke(), C(s, 1, 1, () => {
        s = null;
      }), ge());
    },
    i(o) {
      l || (I(s), l = !0);
    },
    o(o) {
      C(s), l = !1;
    },
    d(o) {
      o && B(t), s && s.d(o);
    }
  };
}
function Ae(e, t, l) {
  let s, o, n, i, c, a, {
    $$slots: m = {},
    $$scope: _
  } = t;
  const d = W(() => import("./table-CgaVVYTE.js"));
  let {
    gradio: b
  } = t, {
    _internal: u = {}
  } = t, {
    as_item: h
  } = t, {
    props: k = {}
  } = t, {
    data_source: K
  } = t;
  const F = g(k);
  S(e, F, (r) => l(21, s = r));
  let {
    elem_id: x = ""
  } = t, {
    elem_classes: P = []
  } = t, {
    elem_style: v = {}
  } = t, {
    visible: j = !0
  } = t;
  const q = ne();
  S(e, q, (r) => l(1, n = r));
  const [A, J] = oe({
    gradio: b,
    props: s,
    _internal: u,
    as_item: h,
    visible: j,
    elem_id: x,
    elem_classes: P,
    elem_style: v,
    data_source: K
  });
  S(e, A, (r) => l(0, o = r));
  const {
    rowSelection: R
  } = fe(["rowSelection"]);
  S(e, R, (r) => l(2, i = r));
  const {
    expandable: M
  } = de(["expandable"]);
  S(e, M, (r) => l(3, c = r));
  const {
    default: V
  } = _e();
  return S(e, V, (r) => l(4, a = r)), e.$$set = (r) => {
    "gradio" in r && l(12, b = r.gradio), "_internal" in r && l(13, u = r._internal), "as_item" in r && l(14, h = r.as_item), "props" in r && l(15, k = r.props), "data_source" in r && l(16, K = r.data_source), "elem_id" in r && l(17, x = r.elem_id), "elem_classes" in r && l(18, P = r.elem_classes), "elem_style" in r && l(19, v = r.elem_style), "visible" in r && l(20, j = r.visible), "$$scope" in r && l(23, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    32768 && F.update((r) => ({
      ...r,
      ...k
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, as_item, visible, elem_id, elem_classes, elem_style, data_source*/
    4157440 && J({
      gradio: b,
      props: s,
      _internal: u,
      as_item: h,
      visible: j,
      elem_id: x,
      elem_classes: P,
      elem_style: v,
      data_source: K
    });
  }, [o, n, i, c, a, d, F, q, A, R, M, V, b, u, h, k, K, x, P, v, j, s, m, _];
}
class Xe extends be {
  constructor(t) {
    super(), xe(this, t, Ae, qe, ve, {
      gradio: 12,
      _internal: 13,
      as_item: 14,
      props: 15,
      data_source: 16,
      elem_id: 17,
      elem_classes: 18,
      elem_style: 19,
      visible: 20
    });
  }
  get gradio() {
    return this.$$.ctx[12];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[13];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[14];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get props() {
    return this.$$.ctx[15];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get data_source() {
    return this.$$.ctx[16];
  }
  set data_source(t) {
    this.$$set({
      data_source: t
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[17];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[18];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[19];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[20];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), p();
  }
}
export {
  Xe as I,
  Re as g,
  g as w
};
