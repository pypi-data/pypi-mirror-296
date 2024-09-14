async function G() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((n) => {
    window.ms_globals.initialize = () => {
      n();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(n) {
  return await G(), n().then((e) => e.default);
}
function R(n) {
  const {
    gradio: e,
    _internal: l,
    ...t
  } = n;
  return Object.keys(l).reduce((o, s) => {
    const i = s.match(/bind_(.+)_event/);
    if (i) {
      const a = i[1], r = a.split("_"), u = (...d) => {
        const h = d.map((_) => d && typeof _ == "object" && (_.nativeEvent || _ instanceof Event) ? {
          type: _.type,
          detail: _.detail,
          timestamp: _.timeStamp,
          clientX: _.clientX,
          clientY: _.clientY,
          targetId: _.target.id,
          targetClassName: _.target.className,
          altKey: _.altKey,
          ctrlKey: _.ctrlKey,
          shiftKey: _.shiftKey,
          metaKey: _.metaKey
        } : _);
        return e.dispatch(a.replace(/[A-Z]/g, (_) => "_" + _.toLowerCase()), {
          payload: h,
          component: t
        });
      };
      if (r.length > 1) {
        let d = {
          ...t.props[r[0]] || {}
        };
        o[r[0]] = d;
        for (let _ = 1; _ < r.length - 1; _++) {
          const p = {
            ...t.props[r[_]] || {}
          };
          d[r[_]] = p, d = p;
        }
        const h = r[r.length - 1];
        return d[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = u, o;
      }
      const m = r[0];
      o[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = u;
    }
    return o;
  }, {});
}
function j() {
}
function J(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function Q(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return j;
  }
  const l = n.subscribe(...e);
  return l.unsubscribe ? () => l.unsubscribe() : l;
}
function w(n) {
  let e;
  return Q(n, (l) => e = l)(), e;
}
const C = [];
function y(n, e = j) {
  let l;
  const t = /* @__PURE__ */ new Set();
  function o(a) {
    if (J(n, a) && (n = a, l)) {
      const r = !C.length;
      for (const u of t)
        u[1](), C.push(u, n);
      if (r) {
        for (let u = 0; u < C.length; u += 2)
          C[u][0](C[u + 1]);
        C.length = 0;
      }
    }
  }
  function s(a) {
    o(a(n));
  }
  function i(a, r = j) {
    const u = [a, r];
    return t.add(u), t.size === 1 && (l = e(o, s) || j), a(n), () => {
      t.delete(u), t.size === 0 && l && (l(), l = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: i
  };
}
const {
  getContext: O,
  setContext: q
} = window.__gradio__svelte__internal, W = "$$ms-gr-antd-slots-key";
function $() {
  const n = y({});
  return q(W, n);
}
const ee = "$$ms-gr-antd-context-key";
function te(n) {
  var a;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = se(), l = le({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((r) => {
    l.slotKey.set(r);
  }), ne();
  const t = O(ee), o = ((a = w(t)) == null ? void 0 : a.as_item) || n.as_item, s = t ? o ? w(t)[o] : w(t) : {}, i = y({
    ...n,
    ...s
  });
  return t ? (t.subscribe((r) => {
    const {
      as_item: u
    } = w(i);
    u && (r = r[u]), i.update((m) => ({
      ...m,
      ...r
    }));
  }), [i, (r) => {
    const u = r.as_item ? w(t)[r.as_item] : w(t);
    return i.set({
      ...r,
      ...u
    });
  }]) : [i, (r) => {
    i.set(r);
  }];
}
const D = "$$ms-gr-antd-slot-key";
function ne() {
  q(D, y(void 0));
}
function se() {
  return O(D);
}
const F = "$$ms-gr-antd-component-slot-context-key";
function le({
  slot: n,
  index: e,
  subIndex: l
}) {
  return q(F, {
    slotKey: y(n),
    slotIndex: y(e),
    subSlotIndex: y(l)
  });
}
function Ee() {
  return O(F);
}
function oe(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var L = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var e = {}.hasOwnProperty;
    function l() {
      for (var s = "", i = 0; i < arguments.length; i++) {
        var a = arguments[i];
        a && (s = o(s, t(a)));
      }
      return s;
    }
    function t(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return l.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var i = "";
      for (var a in s)
        e.call(s, a) && s[a] && (i = o(i, a));
      return i;
    }
    function o(s, i) {
      return i ? s ? s + " " + i : s + i : s;
    }
    n.exports ? (l.default = l, n.exports = l) : window.classNames = l;
  })();
})(L);
var ie = L.exports;
const U = /* @__PURE__ */ oe(ie), {
  SvelteComponent: re,
  assign: ce,
  check_outros: M,
  component_subscribe: E,
  create_component: ue,
  create_slot: ae,
  destroy_component: _e,
  detach: z,
  empty: A,
  flush: b,
  get_all_dirty_from_scope: fe,
  get_slot_changes: me,
  get_spread_object: X,
  get_spread_update: de,
  group_outros: T,
  handle_promise: be,
  init: he,
  insert: I,
  mount_component: pe,
  noop: f,
  safe_not_equal: ge,
  set_data: ye,
  text: ke,
  transition_in: g,
  transition_out: k,
  update_await_block_branch: we,
  update_slot_base: Ce
} = window.__gradio__svelte__internal;
function Y(n) {
  let e, l, t = {
    ctx: n,
    current: null,
    token: null,
    hasCatch: !1,
    pending: je,
    then: Ke,
    catch: ve,
    value: 21,
    blocks: [, , ,]
  };
  return be(
    /*AwaitedCheckableTag*/
    n[3],
    t
  ), {
    c() {
      e = A(), t.block.c();
    },
    m(o, s) {
      I(o, e, s), t.block.m(o, t.anchor = s), t.mount = () => e.parentNode, t.anchor = e, l = !0;
    },
    p(o, s) {
      n = o, we(t, n, s);
    },
    i(o) {
      l || (g(t.block), l = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const i = t.blocks[s];
        k(i);
      }
      l = !1;
    },
    d(o) {
      o && z(e), t.block.d(o), t.token = null, t = null;
    }
  };
}
function ve(n) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ke(n) {
  let e, l;
  const t = [
    {
      style: (
        /*$mergedProps*/
        n[1].elem_style
      )
    },
    {
      className: U(
        /*$mergedProps*/
        n[1].elem_classes,
        "ms-gr-antd-tag-checkable-tag"
      )
    },
    {
      id: (
        /*$mergedProps*/
        n[1].elem_id
      )
    },
    /*$mergedProps*/
    n[1].props,
    R(
      /*$mergedProps*/
      n[1]
    ),
    {
      slots: (
        /*$slots*/
        n[2]
      )
    },
    {
      checked: (
        /*$mergedProps*/
        n[1].props.checked ?? /*$mergedProps*/
        n[1].value
      )
    },
    {
      onValueChange: (
        /*func*/
        n[18]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Ne]
    },
    $$scope: {
      ctx: n
    }
  };
  for (let s = 0; s < t.length; s += 1)
    o = ce(o, t[s]);
  return e = new /*CheckableTag*/
  n[21]({
    props: o
  }), {
    c() {
      ue(e.$$.fragment);
    },
    m(s, i) {
      pe(e, s, i), l = !0;
    },
    p(s, i) {
      const a = i & /*$mergedProps, $slots, value*/
      7 ? de(t, [i & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          s[1].elem_style
        )
      }, i & /*$mergedProps*/
      2 && {
        className: U(
          /*$mergedProps*/
          s[1].elem_classes,
          "ms-gr-antd-tag-checkable-tag"
        )
      }, i & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          s[1].elem_id
        )
      }, i & /*$mergedProps*/
      2 && X(
        /*$mergedProps*/
        s[1].props
      ), i & /*$mergedProps*/
      2 && X(R(
        /*$mergedProps*/
        s[1]
      )), i & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          s[2]
        )
      }, i & /*$mergedProps*/
      2 && {
        checked: (
          /*$mergedProps*/
          s[1].props.checked ?? /*$mergedProps*/
          s[1].value
        )
      }, i & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          s[18]
        )
      }]) : {};
      i & /*$$scope, $mergedProps*/
      524290 && (a.$$scope = {
        dirty: i,
        ctx: s
      }), e.$set(a);
    },
    i(s) {
      l || (g(e.$$.fragment, s), l = !0);
    },
    o(s) {
      k(e.$$.fragment, s), l = !1;
    },
    d(s) {
      _e(e, s);
    }
  };
}
function Se(n) {
  let e = (
    /*$mergedProps*/
    n[1].label + ""
  ), l;
  return {
    c() {
      l = ke(e);
    },
    m(t, o) {
      I(t, l, o);
    },
    p(t, o) {
      o & /*$mergedProps*/
      2 && e !== (e = /*$mergedProps*/
      t[1].label + "") && ye(l, e);
    },
    i: f,
    o: f,
    d(t) {
      t && z(l);
    }
  };
}
function Pe(n) {
  let e;
  const l = (
    /*#slots*/
    n[17].default
  ), t = ae(
    l,
    n,
    /*$$scope*/
    n[19],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(o, s) {
      t && t.m(o, s), e = !0;
    },
    p(o, s) {
      t && t.p && (!e || s & /*$$scope*/
      524288) && Ce(
        t,
        l,
        o,
        /*$$scope*/
        o[19],
        e ? me(
          l,
          /*$$scope*/
          o[19],
          s,
          null
        ) : fe(
          /*$$scope*/
          o[19]
        ),
        null
      );
    },
    i(o) {
      e || (g(t, o), e = !0);
    },
    o(o) {
      k(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function Ne(n) {
  let e, l, t, o;
  const s = [Pe, Se], i = [];
  function a(r, u) {
    return (
      /*$mergedProps*/
      r[1]._internal.layout ? 0 : 1
    );
  }
  return e = a(n), l = i[e] = s[e](n), {
    c() {
      l.c(), t = A();
    },
    m(r, u) {
      i[e].m(r, u), I(r, t, u), o = !0;
    },
    p(r, u) {
      let m = e;
      e = a(r), e === m ? i[e].p(r, u) : (T(), k(i[m], 1, 1, () => {
        i[m] = null;
      }), M(), l = i[e], l ? l.p(r, u) : (l = i[e] = s[e](r), l.c()), g(l, 1), l.m(t.parentNode, t));
    },
    i(r) {
      o || (g(l), o = !0);
    },
    o(r) {
      k(l), o = !1;
    },
    d(r) {
      r && z(t), i[e].d(r);
    }
  };
}
function je(n) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function ze(n) {
  let e, l, t = (
    /*$mergedProps*/
    n[1].visible && Y(n)
  );
  return {
    c() {
      t && t.c(), e = A();
    },
    m(o, s) {
      t && t.m(o, s), I(o, e, s), l = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[1].visible ? t ? (t.p(o, s), s & /*$mergedProps*/
      2 && g(t, 1)) : (t = Y(o), t.c(), g(t, 1), t.m(e.parentNode, e)) : t && (T(), k(t, 1, 1, () => {
        t = null;
      }), M());
    },
    i(o) {
      l || (g(t), l = !0);
    },
    o(o) {
      k(t), l = !1;
    },
    d(o) {
      o && z(e), t && t.d(o);
    }
  };
}
function Ie(n, e, l) {
  let t, o, s, {
    $$slots: i = {},
    $$scope: a
  } = e;
  const r = H(() => import("./tag.checkable-tag-l6oDkYrh.js"));
  let {
    gradio: u
  } = e, {
    props: m = {}
  } = e;
  const d = y(m);
  E(n, d, (c) => l(16, t = c));
  let {
    _internal: h = {}
  } = e, {
    as_item: _
  } = e, {
    value: p = !1
  } = e, {
    label: v = ""
  } = e, {
    visible: K = !0
  } = e, {
    elem_id: S = ""
  } = e, {
    elem_classes: P = []
  } = e, {
    elem_style: N = {}
  } = e;
  const [x, Z] = te({
    gradio: u,
    props: t,
    _internal: h,
    visible: K,
    elem_id: S,
    elem_classes: P,
    elem_style: N,
    as_item: _,
    value: p,
    label: v
  });
  E(n, x, (c) => l(1, o = c));
  const V = $();
  E(n, V, (c) => l(2, s = c));
  const B = (c) => {
    l(0, p = c);
  };
  return n.$$set = (c) => {
    "gradio" in c && l(7, u = c.gradio), "props" in c && l(8, m = c.props), "_internal" in c && l(9, h = c._internal), "as_item" in c && l(10, _ = c.as_item), "value" in c && l(0, p = c.value), "label" in c && l(11, v = c.label), "visible" in c && l(12, K = c.visible), "elem_id" in c && l(13, S = c.elem_id), "elem_classes" in c && l(14, P = c.elem_classes), "elem_style" in c && l(15, N = c.elem_style), "$$scope" in c && l(19, a = c.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    256 && d.update((c) => ({
      ...c,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value, label*/
    130689 && Z({
      gradio: u,
      props: t,
      _internal: h,
      visible: K,
      elem_id: S,
      elem_classes: P,
      elem_style: N,
      as_item: _,
      value: p,
      label: v
    });
  }, [p, o, s, r, d, x, V, u, m, h, _, v, K, S, P, N, t, i, B, a];
}
class Oe extends re {
  constructor(e) {
    super(), he(this, e, Ie, ze, ge, {
      gradio: 7,
      props: 8,
      _internal: 9,
      as_item: 10,
      value: 0,
      label: 11,
      visible: 12,
      elem_id: 13,
      elem_classes: 14,
      elem_style: 15
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), b();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), b();
  }
  get label() {
    return this.$$.ctx[11];
  }
  set label(e) {
    this.$$set({
      label: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[12];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[13];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[14];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[15];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  Oe as I,
  Ee as g,
  y as w
};
