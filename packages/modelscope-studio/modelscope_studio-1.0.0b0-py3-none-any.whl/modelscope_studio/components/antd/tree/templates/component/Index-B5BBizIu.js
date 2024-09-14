async function H() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function J(e) {
  return await H(), e().then((n) => n.default);
}
function F(e) {
  const {
    gradio: n,
    _internal: l,
    ...s
  } = e;
  return Object.keys(l).reduce((o, t) => {
    const i = t.match(/bind_(.+)_event/);
    if (i) {
      const c = i[1], u = c.split("_"), _ = (...d) => {
        const p = d.map((a) => d && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return n.dispatch(c.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (u.length > 1) {
        let d = {
          ...s.props[u[0]] || {}
        };
        o[u[0]] = d;
        for (let a = 1; a < u.length - 1; a++) {
          const y = {
            ...s.props[u[a]] || {}
          };
          d[u[a]] = y, d = y;
        }
        const p = u[u.length - 1];
        return d[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, o;
      }
      const f = u[0];
      o[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function z() {
}
function Q(e, n) {
  return e != e ? n == n : e !== n || e && typeof e == "object" || typeof e == "function";
}
function W(e, ...n) {
  if (e == null) {
    for (const s of n)
      s(void 0);
    return z;
  }
  const l = e.subscribe(...n);
  return l.unsubscribe ? () => l.unsubscribe() : l;
}
function g(e) {
  let n;
  return W(e, (l) => n = l)(), n;
}
const k = [];
function b(e, n = z) {
  let l;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (Q(e, c) && (e = c, l)) {
      const u = !k.length;
      for (const _ of s)
        _[1](), k.push(_, e);
      if (u) {
        for (let _ = 0; _ < k.length; _ += 2)
          k[_][0](k[_ + 1]);
        k.length = 0;
      }
    }
  }
  function t(c) {
    o(c(e));
  }
  function i(c, u = z) {
    const _ = [c, u];
    return s.add(_), s.size === 1 && (l = n(o, t) || z), c(e), () => {
      s.delete(_), s.size === 0 && l && (l(), l = null);
    };
  }
  return {
    set: o,
    update: t,
    subscribe: i
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = b({});
  return O($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = oe(), l = le({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  n && n.subscribe((u) => {
    l.slotKey.set(u);
  }), se();
  const s = E(te), o = ((c = g(s)) == null ? void 0 : c.as_item) || e.as_item, t = s ? o ? g(s)[o] : g(s) : {}, i = b({
    ...e,
    ...t
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: _
    } = g(i);
    _ && (u = u[_]), i.update((f) => ({
      ...f,
      ...u
    }));
  }), [i, (u) => {
    const _ = u.as_item ? g(s)[u.as_item] : g(s);
    return i.set({
      ...u,
      ..._
    });
  }]) : [i, (u) => {
    i.set(u);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function se() {
  O(X, b(void 0));
}
function oe() {
  return E(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function le({
  slot: e,
  index: n,
  subIndex: l
}) {
  return O(Y, {
    slotKey: b(e),
    slotIndex: b(n),
    subSlotIndex: b(l)
  });
}
function qe() {
  return E(Y);
}
function ie(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var x = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var n = {}.hasOwnProperty;
    function l() {
      for (var t = "", i = 0; i < arguments.length; i++) {
        var c = arguments[i];
        c && (t = o(t, s(c)));
      }
      return t;
    }
    function s(t) {
      if (typeof t == "string" || typeof t == "number")
        return t;
      if (typeof t != "object")
        return "";
      if (Array.isArray(t))
        return l.apply(null, t);
      if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]"))
        return t.toString();
      var i = "";
      for (var c in t)
        n.call(t, c) && t[c] && (i = o(i, c));
      return i;
    }
    function o(t, i) {
      return i ? t ? t + " " + i : t + i : t;
    }
    e.exports ? (l.default = l, e.exports = l) : window.classNames = l;
  })();
})(x);
var re = x.exports;
const M = /* @__PURE__ */ ie(re), {
  getContext: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ae(e) {
  const n = `$$ms-gr-antd-${e}-context-key`;
  function l(o = ["default"]) {
    const t = o.reduce((i, c) => (i[c] = b([]), i), {});
    return ue(n, {
      itemsMap: t,
      allowedSlots: o
    }), t;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: t
    } = ce(n);
    return function(i, c, u) {
      o && (i ? o[i].update((_) => {
        const f = [..._];
        return t.includes(i) ? f[c] = u : f[c] = void 0, f;
      }) : t.includes("default") && o.default.update((_) => {
        const f = [..._];
        return f[c] = u, f;
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
  getSetItemFn: Ae
} = ae("tree"), {
  SvelteComponent: fe,
  assign: de,
  check_outros: me,
  component_subscribe: C,
  create_component: pe,
  create_slot: he,
  destroy_component: be,
  detach: L,
  empty: T,
  flush: h,
  get_all_dirty_from_scope: ye,
  get_slot_changes: ge,
  get_spread_object: R,
  get_spread_update: ke,
  group_outros: we,
  handle_promise: Ke,
  init: Ce,
  insert: Z,
  mount_component: ve,
  noop: m,
  safe_not_equal: Se,
  transition_in: w,
  transition_out: v,
  update_await_block_branch: Ie,
  update_slot_base: Pe
} = window.__gradio__svelte__internal;
function U(e) {
  let n, l, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ee,
    then: Ne,
    catch: je,
    value: 24,
    blocks: [, , ,]
  };
  return Ke(
    /*AwaitedTree*/
    e[4],
    s
  ), {
    c() {
      n = T(), s.block.c();
    },
    m(o, t) {
      Z(o, n, t), s.block.m(o, s.anchor = t), s.mount = () => n.parentNode, s.anchor = n, l = !0;
    },
    p(o, t) {
      e = o, Ie(s, e, t);
    },
    i(o) {
      l || (w(s.block), l = !0);
    },
    o(o) {
      for (let t = 0; t < 3; t += 1) {
        const i = s.blocks[t];
        v(i);
      }
      l = !1;
    },
    d(o) {
      o && L(n), s.block.d(o), s.token = null, s = null;
    }
  };
}
function je(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Ne(e) {
  let n, l;
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
        "ms-gr-antd-tree"
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
        /*$treeData*/
        e[2].length ? (
          /*$treeData*/
          e[2]
        ) : (
          /*$children*/
          e[3]
        )
      )
    },
    {
      selectedKeys: (
        /*$mergedProps*/
        e[0].props.selectedKeys || /*$mergedProps*/
        e[0].value.selected_keys
      )
    },
    {
      expandedKeys: (
        /*$mergedProps*/
        e[0].props.expandedKeys || /*$mergedProps*/
        e[0].value.expanded_keys
      )
    },
    {
      checkedKeys: (
        /*$mergedProps*/
        e[0].props.checkedKeys || /*$mergedProps*/
        e[0].value.checked_keys
      )
    },
    {
      onValueChange: (
        /*onValueChange*/
        e[10]
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
  for (let t = 0; t < s.length; t += 1)
    o = de(o, s[t]);
  return n = new /*Tree*/
  e[24]({
    props: o
  }), {
    c() {
      pe(n.$$.fragment);
    },
    m(t, i) {
      ve(n, t, i), l = !0;
    },
    p(t, i) {
      const c = i & /*$mergedProps, $slots, $treeData, $children, onValueChange*/
      1039 ? ke(s, [i & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          t[0].elem_style
        )
      }, i & /*$mergedProps*/
      1 && {
        className: M(
          /*$mergedProps*/
          t[0].elem_classes,
          "ms-gr-antd-tree"
        )
      }, i & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          t[0].elem_id
        )
      }, i & /*$mergedProps*/
      1 && R(
        /*$mergedProps*/
        t[0].props
      ), i & /*$mergedProps*/
      1 && R(F(
        /*$mergedProps*/
        t[0]
      )), i & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          t[1]
        )
      }, i & /*$treeData, $children*/
      12 && {
        slotItems: (
          /*$treeData*/
          t[2].length ? (
            /*$treeData*/
            t[2]
          ) : (
            /*$children*/
            t[3]
          )
        )
      }, i & /*$mergedProps*/
      1 && {
        selectedKeys: (
          /*$mergedProps*/
          t[0].props.selectedKeys || /*$mergedProps*/
          t[0].value.selected_keys
        )
      }, i & /*$mergedProps*/
      1 && {
        expandedKeys: (
          /*$mergedProps*/
          t[0].props.expandedKeys || /*$mergedProps*/
          t[0].value.expanded_keys
        )
      }, i & /*$mergedProps*/
      1 && {
        checkedKeys: (
          /*$mergedProps*/
          t[0].props.checkedKeys || /*$mergedProps*/
          t[0].value.checked_keys
        )
      }, i & /*onValueChange*/
      1024 && {
        onValueChange: (
          /*onValueChange*/
          t[10]
        )
      }]) : {};
      i & /*$$scope*/
      4194304 && (c.$$scope = {
        dirty: i,
        ctx: t
      }), n.$set(c);
    },
    i(t) {
      l || (w(n.$$.fragment, t), l = !0);
    },
    o(t) {
      v(n.$$.fragment, t), l = !1;
    },
    d(t) {
      be(n, t);
    }
  };
}
function ze(e) {
  let n;
  const l = (
    /*#slots*/
    e[21].default
  ), s = he(
    l,
    e,
    /*$$scope*/
    e[22],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(o, t) {
      s && s.m(o, t), n = !0;
    },
    p(o, t) {
      s && s.p && (!n || t & /*$$scope*/
      4194304) && Pe(
        s,
        l,
        o,
        /*$$scope*/
        o[22],
        n ? ge(
          l,
          /*$$scope*/
          o[22],
          t,
          null
        ) : ye(
          /*$$scope*/
          o[22]
        ),
        null
      );
    },
    i(o) {
      n || (w(s, o), n = !0);
    },
    o(o) {
      v(s, o), n = !1;
    },
    d(o) {
      s && s.d(o);
    }
  };
}
function Ee(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function Oe(e) {
  let n, l, s = (
    /*$mergedProps*/
    e[0].visible && U(e)
  );
  return {
    c() {
      s && s.c(), n = T();
    },
    m(o, t) {
      s && s.m(o, t), Z(o, n, t), l = !0;
    },
    p(o, [t]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, t), t & /*$mergedProps*/
      1 && w(s, 1)) : (s = U(o), s.c(), w(s, 1), s.m(n.parentNode, n)) : s && (we(), v(s, 1, 1, () => {
        s = null;
      }), me());
    },
    i(o) {
      l || (w(s), l = !0);
    },
    o(o) {
      v(s), l = !1;
    },
    d(o) {
      o && L(n), s && s.d(o);
    }
  };
}
function Ve(e, n, l) {
  let s, o, t, i, c, {
    $$slots: u = {},
    $$scope: _
  } = n;
  const f = J(() => import("./tree-Dn4cxfYb.js"));
  let {
    gradio: d
  } = n, {
    props: p = {}
  } = n;
  const a = b(p);
  C(e, a, (r) => l(20, s = r));
  let {
    _internal: y = {}
  } = n, {
    value: K = {}
  } = n, {
    as_item: S
  } = n, {
    visible: I = !0
  } = n, {
    elem_id: P = ""
  } = n, {
    elem_classes: j = []
  } = n, {
    elem_style: N = {}
  } = n;
  const [V, B] = ne({
    gradio: d,
    props: s,
    _internal: y,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: S,
    value: K
  });
  C(e, V, (r) => l(0, o = r));
  const q = ee();
  C(e, q, (r) => l(1, t = r));
  const {
    treeData: A,
    default: D
  } = _e(["default", "treeData"]);
  C(e, A, (r) => l(2, i = r)), C(e, D, (r) => l(3, c = r));
  const G = (r) => {
    l(11, K = {
      expanded_keys: r.expandedKeys,
      checked_keys: r.checkedKeys,
      selected_keys: r.selectedKeys
    });
  };
  return e.$$set = (r) => {
    "gradio" in r && l(12, d = r.gradio), "props" in r && l(13, p = r.props), "_internal" in r && l(14, y = r._internal), "value" in r && l(11, K = r.value), "as_item" in r && l(15, S = r.as_item), "visible" in r && l(16, I = r.visible), "elem_id" in r && l(17, P = r.elem_id), "elem_classes" in r && l(18, j = r.elem_classes), "elem_style" in r && l(19, N = r.elem_style), "$$scope" in r && l(22, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    8192 && a.update((r) => ({
      ...r,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    2086912 && B({
      gradio: d,
      props: s,
      _internal: y,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: S,
      value: K
    });
  }, [o, t, i, c, f, a, V, q, A, D, G, K, d, p, y, S, I, P, j, N, s, u, _];
}
class De extends fe {
  constructor(n) {
    super(), Ce(this, n, Ve, Oe, Se, {
      gradio: 12,
      props: 13,
      _internal: 14,
      value: 11,
      as_item: 15,
      visible: 16,
      elem_id: 17,
      elem_classes: 18,
      elem_style: 19
    });
  }
  get gradio() {
    return this.$$.ctx[12];
  }
  set gradio(n) {
    this.$$set({
      gradio: n
    }), h();
  }
  get props() {
    return this.$$.ctx[13];
  }
  set props(n) {
    this.$$set({
      props: n
    }), h();
  }
  get _internal() {
    return this.$$.ctx[14];
  }
  set _internal(n) {
    this.$$set({
      _internal: n
    }), h();
  }
  get value() {
    return this.$$.ctx[11];
  }
  set value(n) {
    this.$$set({
      value: n
    }), h();
  }
  get as_item() {
    return this.$$.ctx[15];
  }
  set as_item(n) {
    this.$$set({
      as_item: n
    }), h();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(n) {
    this.$$set({
      visible: n
    }), h();
  }
  get elem_id() {
    return this.$$.ctx[17];
  }
  set elem_id(n) {
    this.$$set({
      elem_id: n
    }), h();
  }
  get elem_classes() {
    return this.$$.ctx[18];
  }
  set elem_classes(n) {
    this.$$set({
      elem_classes: n
    }), h();
  }
  get elem_style() {
    return this.$$.ctx[19];
  }
  set elem_style(n) {
    this.$$set({
      elem_style: n
    }), h();
  }
}
export {
  De as I,
  qe as g,
  b as w
};
