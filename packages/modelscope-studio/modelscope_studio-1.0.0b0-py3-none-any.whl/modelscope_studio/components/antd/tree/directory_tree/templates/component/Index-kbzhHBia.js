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
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, t) => {
    const l = t.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], u = c.split("_"), _ = (...d) => {
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
          const b = {
            ...s.props[u[a]] || {}
          };
          d[u[a]] = b, d = b;
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
  const i = e.subscribe(...n);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function g(e) {
  let n;
  return W(e, (i) => n = i)(), n;
}
const k = [];
function h(e, n = z) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (Q(e, c) && (e = c, i)) {
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
  function l(c, u = z) {
    const _ = [c, u];
    return s.add(_), s.size === 1 && (i = n(o, t) || z), c(e), () => {
      s.delete(_), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: t,
    subscribe: l
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, $ = "$$ms-gr-antd-slots-key";
function ee() {
  const e = h({});
  return O($, e);
}
const te = "$$ms-gr-antd-context-key";
function ne(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const n = oe(), i = ie({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  n && n.subscribe((u) => {
    i.slotKey.set(u);
  }), se();
  const s = E(te), o = ((c = g(s)) == null ? void 0 : c.as_item) || e.as_item, t = s ? o ? g(s)[o] : g(s) : {}, l = h({
    ...e,
    ...t
  });
  return s ? (s.subscribe((u) => {
    const {
      as_item: _
    } = g(l);
    _ && (u = u[_]), l.update((f) => ({
      ...f,
      ...u
    }));
  }), [l, (u) => {
    const _ = u.as_item ? g(s)[u.as_item] : g(s);
    return l.set({
      ...u,
      ..._
    });
  }]) : [l, (u) => {
    l.set(u);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function se() {
  O(X, h(void 0));
}
function oe() {
  return E(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function ie({
  slot: e,
  index: n,
  subIndex: i
}) {
  return O(Y, {
    slotKey: h(e),
    slotIndex: h(n),
    subSlotIndex: h(i)
  });
}
function qe() {
  return E(Y);
}
function le(e) {
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
    function i() {
      for (var t = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
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
        return i.apply(null, t);
      if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]"))
        return t.toString();
      var l = "";
      for (var c in t)
        n.call(t, c) && t[c] && (l = o(l, c));
      return l;
    }
    function o(t, l) {
      return l ? t ? t + " " + l : t + l : t;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(x);
var re = x.exports;
const M = /* @__PURE__ */ le(re), {
  getContext: ce,
  setContext: ue
} = window.__gradio__svelte__internal;
function ae(e) {
  const n = `$$ms-gr-antd-${e}-context-key`;
  function i(o = ["default"]) {
    const t = o.reduce((l, c) => (l[c] = h([]), l), {});
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
    return function(l, c, u) {
      o && (l ? o[l].update((_) => {
        const f = [..._];
        return t.includes(l) ? f[c] = u : f[c] = void 0, f;
      }) : t.includes("default") && o.default.update((_) => {
        const f = [..._];
        return f[c] = u, f;
      }));
    };
  }
  return {
    getItems: i,
    getSetItemFn: s
  };
}
const {
  getItems: _e,
  getSetItemFn: De
} = ae("tree"), {
  SvelteComponent: fe,
  assign: de,
  check_outros: me,
  component_subscribe: C,
  create_component: pe,
  create_slot: ye,
  destroy_component: he,
  detach: L,
  empty: T,
  flush: y,
  get_all_dirty_from_scope: be,
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
  let n, i, s = {
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
    /*AwaitedDirectoryTree*/
    e[4],
    s
  ), {
    c() {
      n = T(), s.block.c();
    },
    m(o, t) {
      Z(o, n, t), s.block.m(o, s.anchor = t), s.mount = () => n.parentNode, s.anchor = n, i = !0;
    },
    p(o, t) {
      e = o, Ie(s, e, t);
    },
    i(o) {
      i || (w(s.block), i = !0);
    },
    o(o) {
      for (let t = 0; t < 3; t += 1) {
        const l = s.blocks[t];
        v(l);
      }
      i = !1;
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
  let n, i;
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
        "ms-gr-antd-directory-tree"
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
      directory: !0
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
  return n = new /*DirectoryTree*/
  e[24]({
    props: o
  }), {
    c() {
      pe(n.$$.fragment);
    },
    m(t, l) {
      ve(n, t, l), i = !0;
    },
    p(t, l) {
      const c = l & /*$mergedProps, $slots, $treeData, $children, onValueChange*/
      1039 ? ke(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          t[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: M(
          /*$mergedProps*/
          t[0].elem_classes,
          "ms-gr-antd-directory-tree"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          t[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && R(
        /*$mergedProps*/
        t[0].props
      ), l & /*$mergedProps*/
      1 && R(F(
        /*$mergedProps*/
        t[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          t[1]
        )
      }, s[6], l & /*$treeData, $children*/
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
      }, l & /*$mergedProps*/
      1 && {
        selectedKeys: (
          /*$mergedProps*/
          t[0].props.selectedKeys || /*$mergedProps*/
          t[0].value.selected_keys
        )
      }, l & /*$mergedProps*/
      1 && {
        expandedKeys: (
          /*$mergedProps*/
          t[0].props.expandedKeys || /*$mergedProps*/
          t[0].value.expanded_keys
        )
      }, l & /*$mergedProps*/
      1 && {
        checkedKeys: (
          /*$mergedProps*/
          t[0].props.checkedKeys || /*$mergedProps*/
          t[0].value.checked_keys
        )
      }, l & /*onValueChange*/
      1024 && {
        onValueChange: (
          /*onValueChange*/
          t[10]
        )
      }]) : {};
      l & /*$$scope*/
      4194304 && (c.$$scope = {
        dirty: l,
        ctx: t
      }), n.$set(c);
    },
    i(t) {
      i || (w(n.$$.fragment, t), i = !0);
    },
    o(t) {
      v(n.$$.fragment, t), i = !1;
    },
    d(t) {
      he(n, t);
    }
  };
}
function ze(e) {
  let n;
  const i = (
    /*#slots*/
    e[21].default
  ), s = ye(
    i,
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
        i,
        o,
        /*$$scope*/
        o[22],
        n ? ge(
          i,
          /*$$scope*/
          o[22],
          t,
          null
        ) : be(
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
  let n, i, s = (
    /*$mergedProps*/
    e[0].visible && U(e)
  );
  return {
    c() {
      s && s.c(), n = T();
    },
    m(o, t) {
      s && s.m(o, t), Z(o, n, t), i = !0;
    },
    p(o, [t]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, t), t & /*$mergedProps*/
      1 && w(s, 1)) : (s = U(o), s.c(), w(s, 1), s.m(n.parentNode, n)) : s && (we(), v(s, 1, 1, () => {
        s = null;
      }), me());
    },
    i(o) {
      i || (w(s), i = !0);
    },
    o(o) {
      v(s), i = !1;
    },
    d(o) {
      o && L(n), s && s.d(o);
    }
  };
}
function Ve(e, n, i) {
  let s, o, t, l, c, {
    $$slots: u = {},
    $$scope: _
  } = n;
  const f = J(() => import("./tree-cQ33wkEV.js"));
  let {
    gradio: d
  } = n, {
    props: p = {}
  } = n;
  const a = h(p);
  C(e, a, (r) => i(20, s = r));
  let {
    _internal: b = {}
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
    _internal: b,
    visible: I,
    elem_id: P,
    elem_classes: j,
    elem_style: N,
    as_item: S,
    value: K
  });
  C(e, V, (r) => i(0, o = r));
  const q = ee();
  C(e, q, (r) => i(1, t = r));
  const {
    treeData: D,
    default: A
  } = _e(["default", "treeData"]);
  C(e, D, (r) => i(2, l = r)), C(e, A, (r) => i(3, c = r));
  const G = (r) => {
    i(11, K = {
      expanded_keys: r.expandedKeys,
      checked_keys: r.checkedKeys,
      selected_keys: r.selectedKeys
    });
  };
  return e.$$set = (r) => {
    "gradio" in r && i(12, d = r.gradio), "props" in r && i(13, p = r.props), "_internal" in r && i(14, b = r._internal), "value" in r && i(11, K = r.value), "as_item" in r && i(15, S = r.as_item), "visible" in r && i(16, I = r.visible), "elem_id" in r && i(17, P = r.elem_id), "elem_classes" in r && i(18, j = r.elem_classes), "elem_style" in r && i(19, N = r.elem_style), "$$scope" in r && i(22, _ = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    8192 && a.update((r) => ({
      ...r,
      ...p
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    2086912 && B({
      gradio: d,
      props: s,
      _internal: b,
      visible: I,
      elem_id: P,
      elem_classes: j,
      elem_style: N,
      as_item: S,
      value: K
    });
  }, [o, t, l, c, f, a, V, q, D, A, G, K, d, p, b, S, I, P, j, N, s, u, _];
}
class Ae extends fe {
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
    }), y();
  }
  get props() {
    return this.$$.ctx[13];
  }
  set props(n) {
    this.$$set({
      props: n
    }), y();
  }
  get _internal() {
    return this.$$.ctx[14];
  }
  set _internal(n) {
    this.$$set({
      _internal: n
    }), y();
  }
  get value() {
    return this.$$.ctx[11];
  }
  set value(n) {
    this.$$set({
      value: n
    }), y();
  }
  get as_item() {
    return this.$$.ctx[15];
  }
  set as_item(n) {
    this.$$set({
      as_item: n
    }), y();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(n) {
    this.$$set({
      visible: n
    }), y();
  }
  get elem_id() {
    return this.$$.ctx[17];
  }
  set elem_id(n) {
    this.$$set({
      elem_id: n
    }), y();
  }
  get elem_classes() {
    return this.$$.ctx[18];
  }
  set elem_classes(n) {
    this.$$set({
      elem_classes: n
    }), y();
  }
  get elem_style() {
    return this.$$.ctx[19];
  }
  set elem_style(n) {
    this.$$set({
      elem_style: n
    }), y();
  }
}
export {
  Ae as I,
  qe as g,
  h as w
};
