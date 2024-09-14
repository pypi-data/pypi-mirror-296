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
function R(e) {
  const {
    gradio: t,
    _internal: o,
    ...s
  } = e;
  return Object.keys(o).reduce((i, n) => {
    const l = n.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], c = u.split("_"), f = (...m) => {
        const b = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return t.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
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
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, i;
      }
      const _ = c[0];
      i[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function E() {
}
function x(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function $(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return E;
  }
  const o = e.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function y(e) {
  let t;
  return $(e, (o) => t = o)(), t;
}
const w = [];
function h(e, t = E) {
  let o;
  const s = /* @__PURE__ */ new Set();
  function i(u) {
    if (x(e, u) && (e = u, o)) {
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
  function n(u) {
    i(u(e));
  }
  function l(u, c = E) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (o = t(i, n) || E), u(e), () => {
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
  getContext: O,
  setContext: q
} = window.__gradio__svelte__internal, ee = "$$ms-gr-antd-slots-key";
function te() {
  const e = h({});
  return q(ee, e);
}
const ne = "$$ms-gr-antd-context-key";
function se(e) {
  var u;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = ie(), o = le({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((c) => {
    o.slotKey.set(c);
  }), oe();
  const s = O(ne), i = ((u = y(s)) == null ? void 0 : u.as_item) || e.as_item, n = s ? i ? y(s)[i] : y(s) : {}, l = h({
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
const D = "$$ms-gr-antd-slot-key";
function oe() {
  q(D, h(void 0));
}
function ie() {
  return O(D);
}
const L = "$$ms-gr-antd-component-slot-context-key";
function le({
  slot: e,
  index: t,
  subIndex: o
}) {
  return q(L, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(o)
  });
}
function Ae() {
  return O(L);
}
function re(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var T = {
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
        var u = arguments[l];
        u && (n = i(n, s(u)));
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
      for (var u in n)
        t.call(n, u) && n[u] && (l = i(l, u));
      return l;
    }
    function i(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    e.exports ? (o.default = o, e.exports = o) : window.classNames = o;
  })();
})(T);
var ue = T.exports;
const U = /* @__PURE__ */ re(ue), {
  getContext: ce,
  setContext: ae
} = window.__gradio__svelte__internal;
function fe(e) {
  const t = `$$ms-gr-antd-${e}-context-key`;
  function o(i = ["default"]) {
    const n = i.reduce((l, u) => (l[u] = h([]), l), {});
    return ae(t, {
      itemsMap: n,
      allowedSlots: i
    }), n;
  }
  function s() {
    const {
      itemsMap: i,
      allowedSlots: n
    } = ce(t);
    return function(l, u, c) {
      i && (l ? i[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : n.includes("default") && i.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
      }));
    };
  }
  return {
    getItems: o,
    getSetItemFn: s
  };
}
const {
  getItems: _e,
  getSetItemFn: Fe
} = fe("tour"), {
  SvelteComponent: me,
  assign: de,
  check_outros: pe,
  component_subscribe: K,
  create_component: be,
  create_slot: he,
  destroy_component: ge,
  detach: Z,
  empty: B,
  flush: p,
  get_all_dirty_from_scope: ye,
  get_slot_changes: we,
  get_spread_object: X,
  get_spread_update: Ce,
  group_outros: ke,
  handle_promise: Se,
  init: Ke,
  insert: G,
  mount_component: ve,
  noop: d,
  safe_not_equal: Ie,
  transition_in: C,
  transition_out: v,
  update_await_block_branch: Pe,
  update_slot_base: je
} = window.__gradio__svelte__internal;
function Y(e) {
  let t, o, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Oe,
    then: ze,
    catch: Ne,
    value: 25,
    blocks: [, , ,]
  };
  return Se(
    /*AwaitedTour*/
    e[6],
    s
  ), {
    c() {
      t = B(), s.block.c();
    },
    m(i, n) {
      G(i, t, n), s.block.m(i, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, o = !0;
    },
    p(i, n) {
      e = i, Pe(s, e, n);
    },
    i(i) {
      o || (C(s.block), o = !0);
    },
    o(i) {
      for (let n = 0; n < 3; n += 1) {
        const l = s.blocks[n];
        v(l);
      }
      o = !1;
    },
    d(i) {
      i && Z(t), s.block.d(i), s.token = null, s = null;
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
  let t, o;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[2].elem_style
      )
    },
    {
      className: U(
        /*$mergedProps*/
        e[2].elem_classes,
        "ms-gr-antd-tour"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[2].elem_id
      )
    },
    /*$mergedProps*/
    e[2].props,
    R(
      /*$mergedProps*/
      e[2]
    ),
    {
      current: (
        /*$mergedProps*/
        e[2].props.current ?? /*$mergedProps*/
        e[2].value
      )
    },
    {
      open: (
        /*$mergedProps*/
        e[2].props.open ?? /*$mergedProps*/
        e[2].open
      )
    },
    {
      slots: (
        /*$slots*/
        e[3]
      )
    },
    {
      slotItems: (
        /*$steps*/
        e[4].length > 0 ? (
          /*$steps*/
          e[4]
        ) : (
          /*$children*/
          e[5]
        )
      )
    },
    {
      onValueChange: (
        /*func*/
        e[22]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [Ee]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let n = 0; n < s.length; n += 1)
    i = de(i, s[n]);
  return t = new /*Tour*/
  e[25]({
    props: i
  }), {
    c() {
      be(t.$$.fragment);
    },
    m(n, l) {
      ve(t, n, l), o = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, $steps, $children, value, open*/
      63 ? Ce(s, [l & /*$mergedProps*/
      4 && {
        style: (
          /*$mergedProps*/
          n[2].elem_style
        )
      }, l & /*$mergedProps*/
      4 && {
        className: U(
          /*$mergedProps*/
          n[2].elem_classes,
          "ms-gr-antd-tour"
        )
      }, l & /*$mergedProps*/
      4 && {
        id: (
          /*$mergedProps*/
          n[2].elem_id
        )
      }, l & /*$mergedProps*/
      4 && X(
        /*$mergedProps*/
        n[2].props
      ), l & /*$mergedProps*/
      4 && X(R(
        /*$mergedProps*/
        n[2]
      )), l & /*$mergedProps*/
      4 && {
        current: (
          /*$mergedProps*/
          n[2].props.current ?? /*$mergedProps*/
          n[2].value
        )
      }, l & /*$mergedProps*/
      4 && {
        open: (
          /*$mergedProps*/
          n[2].props.open ?? /*$mergedProps*/
          n[2].open
        )
      }, l & /*$slots*/
      8 && {
        slots: (
          /*$slots*/
          n[3]
        )
      }, l & /*$steps, $children*/
      48 && {
        slotItems: (
          /*$steps*/
          n[4].length > 0 ? (
            /*$steps*/
            n[4]
          ) : (
            /*$children*/
            n[5]
          )
        )
      }, l & /*value, open*/
      3 && {
        onValueChange: (
          /*func*/
          n[22]
        )
      }]) : {};
      l & /*$$scope*/
      8388608 && (u.$$scope = {
        dirty: l,
        ctx: n
      }), t.$set(u);
    },
    i(n) {
      o || (C(t.$$.fragment, n), o = !0);
    },
    o(n) {
      v(t.$$.fragment, n), o = !1;
    },
    d(n) {
      ge(t, n);
    }
  };
}
function Ee(e) {
  let t;
  const o = (
    /*#slots*/
    e[21].default
  ), s = he(
    o,
    e,
    /*$$scope*/
    e[23],
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
      8388608) && je(
        s,
        o,
        i,
        /*$$scope*/
        i[23],
        t ? we(
          o,
          /*$$scope*/
          i[23],
          n,
          null
        ) : ye(
          /*$$scope*/
          i[23]
        ),
        null
      );
    },
    i(i) {
      t || (C(s, i), t = !0);
    },
    o(i) {
      v(s, i), t = !1;
    },
    d(i) {
      s && s.d(i);
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
  let t, o, s = (
    /*$mergedProps*/
    e[2].visible && Y(e)
  );
  return {
    c() {
      s && s.c(), t = B();
    },
    m(i, n) {
      s && s.m(i, n), G(i, t, n), o = !0;
    },
    p(i, [n]) {
      /*$mergedProps*/
      i[2].visible ? s ? (s.p(i, n), n & /*$mergedProps*/
      4 && C(s, 1)) : (s = Y(i), s.c(), C(s, 1), s.m(t.parentNode, t)) : s && (ke(), v(s, 1, 1, () => {
        s = null;
      }), pe());
    },
    i(i) {
      o || (C(s), o = !0);
    },
    o(i) {
      v(s), o = !1;
    },
    d(i) {
      i && Z(t), s && s.d(i);
    }
  };
}
function Ve(e, t, o) {
  let s, i, n, l, u, {
    $$slots: c = {},
    $$scope: f
  } = t;
  const _ = W(() => import("./tour-Cv9bHgJc.js"));
  let {
    gradio: m
  } = t, {
    props: b = {}
  } = t;
  const a = h(b);
  K(e, a, (r) => o(20, s = r));
  let {
    _internal: g = {}
  } = t, {
    as_item: I
  } = t, {
    value: k = 0
  } = t, {
    open: S = !0
  } = t, {
    visible: P = !0
  } = t, {
    elem_id: j = ""
  } = t, {
    elem_classes: N = []
  } = t, {
    elem_style: z = {}
  } = t;
  const [V, H] = se({
    gradio: m,
    props: s,
    _internal: g,
    visible: P,
    elem_id: j,
    elem_classes: N,
    elem_style: z,
    as_item: I,
    value: k,
    open: S
  });
  K(e, V, (r) => o(2, i = r));
  const A = te();
  K(e, A, (r) => o(3, n = r));
  const {
    steps: F,
    default: M
  } = _e(["steps", "default"]);
  K(e, F, (r) => o(4, l = r)), K(e, M, (r) => o(5, u = r));
  const J = (r) => {
    o(0, k = r.current), o(1, S = r.open);
  };
  return e.$$set = (r) => {
    "gradio" in r && o(12, m = r.gradio), "props" in r && o(13, b = r.props), "_internal" in r && o(14, g = r._internal), "as_item" in r && o(15, I = r.as_item), "value" in r && o(0, k = r.value), "open" in r && o(1, S = r.open), "visible" in r && o(16, P = r.visible), "elem_id" in r && o(17, j = r.elem_id), "elem_classes" in r && o(18, N = r.elem_classes), "elem_style" in r && o(19, z = r.elem_style), "$$scope" in r && o(23, f = r.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    8192 && a.update((r) => ({
      ...r,
      ...b
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, open*/
    2084867 && H({
      gradio: m,
      props: s,
      _internal: g,
      visible: P,
      elem_id: j,
      elem_classes: N,
      elem_style: z,
      as_item: I,
      value: k,
      open: S
    });
  }, [k, S, i, n, l, u, _, a, V, A, F, M, m, b, g, I, P, j, N, z, s, c, J, f];
}
class Me extends me {
  constructor(t) {
    super(), Ke(this, t, Ve, qe, Ie, {
      gradio: 12,
      props: 13,
      _internal: 14,
      as_item: 15,
      value: 0,
      open: 1,
      visible: 16,
      elem_id: 17,
      elem_classes: 18,
      elem_style: 19
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
  get props() {
    return this.$$.ctx[13];
  }
  set props(t) {
    this.$$set({
      props: t
    }), p();
  }
  get _internal() {
    return this.$$.ctx[14];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), p();
  }
  get as_item() {
    return this.$$.ctx[15];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), p();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(t) {
    this.$$set({
      value: t
    }), p();
  }
  get open() {
    return this.$$.ctx[1];
  }
  set open(t) {
    this.$$set({
      open: t
    }), p();
  }
  get visible() {
    return this.$$.ctx[16];
  }
  set visible(t) {
    this.$$set({
      visible: t
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
}
export {
  Me as I,
  Ae as g,
  h as w
};
