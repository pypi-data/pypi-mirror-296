async function G() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(t) {
  return await G(), t().then((e) => e.default);
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
      const u = l[1], c = u.split("_"), m = (..._) => {
        const p = _.map((a) => _ && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return e.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (c.length > 1) {
        let _ = {
          ...s.props[c[0]] || {}
        };
        o[c[0]] = _;
        for (let a = 1; a < c.length - 1; a++) {
          const g = {
            ...s.props[c[a]] || {}
          };
          _[c[a]] = g, _ = g;
        }
        const p = c[c.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = m, o;
      }
      const f = c[0];
      o[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = m;
    }
    return o;
  }, {});
}
function z() {
}
function J(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Q(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return z;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return Q(t, (i) => e = i)(), e;
}
const w = [];
function h(t, e = z) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (J(t, u) && (t = u, i)) {
      const c = !w.length;
      for (const m of s)
        m[1](), w.push(m, t);
      if (c) {
        for (let m = 0; m < w.length; m += 2)
          w[m][0](w[m + 1]);
        w.length = 0;
      }
    }
  }
  function n(u) {
    o(u(t));
  }
  function l(u, c = z) {
    const m = [u, c];
    return s.add(m), s.size === 1 && (i = e(o, n) || z), u(t), () => {
      s.delete(m), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
  };
}
const {
  getContext: E,
  setContext: O
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const t = h({});
  return O(T, t);
}
const $ = "$$ms-gr-antd-context-key";
function ee(t) {
  var u;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ne(), i = se({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((c) => {
    i.slotKey.set(c);
  }), te();
  const s = E($), o = ((u = y(s)) == null ? void 0 : u.as_item) || t.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...t,
    ...n
  });
  return s ? (s.subscribe((c) => {
    const {
      as_item: m
    } = y(l);
    m && (c = c[m]), l.update((f) => ({
      ...f,
      ...c
    }));
  }), [l, (c) => {
    const m = c.as_item ? y(s)[c.as_item] : y(s);
    return l.set({
      ...c,
      ...m
    });
  }]) : [l, (c) => {
    l.set(c);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function te() {
  O(U, h(void 0));
}
function ne() {
  return E(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: t,
  index: e,
  subIndex: i
}) {
  return O(X, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function Oe() {
  return E(X);
}
function oe(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var Y = {
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
        var u = arguments[l];
        u && (n = o(n, s(u)));
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
      for (var u in n)
        e.call(n, u) && n[u] && (l = o(l, u));
      return l;
    }
    function o(n, l) {
      return l ? n ? n + " " + l : n + l : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(Y);
var ie = Y.exports;
const R = /* @__PURE__ */ oe(ie), {
  getContext: le,
  setContext: re
} = window.__gradio__svelte__internal;
function ue(t) {
  const e = `$$ms-gr-antd-${t}-context-key`;
  function i(o = ["default"]) {
    const n = o.reduce((l, u) => (l[u] = h([]), l), {});
    return re(e, {
      itemsMap: n,
      allowedSlots: o
    }), n;
  }
  function s() {
    const {
      itemsMap: o,
      allowedSlots: n
    } = le(e);
    return function(l, u, c) {
      o && (l ? o[l].update((m) => {
        const f = [...m];
        return n.includes(l) ? f[u] = c : f[u] = void 0, f;
      }) : n.includes("default") && o.default.update((m) => {
        const f = [...m];
        return f[u] = c, f;
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
  getSetItemFn: qe
} = ue("form-item-rule"), {
  SvelteComponent: ae,
  assign: me,
  check_outros: fe,
  component_subscribe: N,
  create_component: _e,
  create_slot: de,
  destroy_component: be,
  detach: D,
  empty: L,
  flush: b,
  get_all_dirty_from_scope: pe,
  get_slot_changes: he,
  get_spread_object: M,
  get_spread_update: ge,
  group_outros: ye,
  handle_promise: we,
  init: Ce,
  insert: Z,
  mount_component: ke,
  noop: d,
  safe_not_equal: Se,
  transition_in: C,
  transition_out: k,
  update_await_block_branch: Ie,
  update_slot_base: Ke
} = window.__gradio__svelte__internal;
function V(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ne,
    then: ve,
    catch: Pe,
    value: 22,
    blocks: [, , ,]
  };
  return we(
    /*AwaitedFormItem*/
    t[3],
    s
  ), {
    c() {
      e = L(), s.block.c();
    },
    m(o, n) {
      Z(o, e, n), s.block.m(o, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, i = !0;
    },
    p(o, n) {
      t = o, Ie(s, t, n);
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
      o && D(e), s.block.d(o), s.token = null, s = null;
    }
  };
}
function Pe(t) {
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
      className: R(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-form-item"
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
      name: (
        /*$mergedProps*/
        t[0].props.name ?? /*$mergedProps*/
        t[0].form_name
      )
    },
    {
      label: (
        /*$mergedProps*/
        t[0].props.label ?? /*$mergedProps*/
        t[0].label
      )
    },
    {
      slots: (
        /*$slots*/
        t[1]
      )
    },
    {
      ruleItems: (
        /*$ruleItems*/
        t[2]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [je]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    o = me(o, s[n]);
  return e = new /*FormItem*/
  t[22]({
    props: o
  }), {
    c() {
      _e(e.$$.fragment);
    },
    m(n, l) {
      ke(e, n, l), i = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, $ruleItems*/
      7 ? ge(s, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: R(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-form-item"
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
      )), l & /*$mergedProps*/
      1 && {
        name: (
          /*$mergedProps*/
          n[0].props.name ?? /*$mergedProps*/
          n[0].form_name
        )
      }, l & /*$mergedProps*/
      1 && {
        label: (
          /*$mergedProps*/
          n[0].props.label ?? /*$mergedProps*/
          n[0].label
        )
      }, l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, l & /*$ruleItems*/
      4 && {
        ruleItems: (
          /*$ruleItems*/
          n[2]
        )
      }]) : {};
      l & /*$$scope*/
      1048576 && (u.$$scope = {
        dirty: l,
        ctx: n
      }), e.$set(u);
    },
    i(n) {
      i || (C(e.$$.fragment, n), i = !0);
    },
    o(n) {
      k(e.$$.fragment, n), i = !1;
    },
    d(n) {
      be(e, n);
    }
  };
}
function je(t) {
  let e;
  const i = (
    /*#slots*/
    t[19].default
  ), s = de(
    i,
    t,
    /*$$scope*/
    t[20],
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
      1048576) && Ke(
        s,
        i,
        o,
        /*$$scope*/
        o[20],
        e ? he(
          i,
          /*$$scope*/
          o[20],
          n,
          null
        ) : pe(
          /*$$scope*/
          o[20]
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
function Ne(t) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function ze(t) {
  let e, i, s = (
    /*$mergedProps*/
    t[0].visible && V(t)
  );
  return {
    c() {
      s && s.c(), e = L();
    },
    m(o, n) {
      s && s.m(o, n), Z(o, e, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && C(s, 1)) : (s = V(o), s.c(), C(s, 1), s.m(e.parentNode, e)) : s && (ye(), k(s, 1, 1, () => {
        s = null;
      }), fe());
    },
    i(o) {
      i || (C(s), i = !0);
    },
    o(o) {
      k(s), i = !1;
    },
    d(o) {
      o && D(e), s && s.d(o);
    }
  };
}
function Ee(t, e, i) {
  let s, o, n, l, {
    $$slots: u = {},
    $$scope: c
  } = e;
  const m = H(() => import("./form.item-Bv122qzx.js"));
  let {
    gradio: f
  } = e, {
    props: _ = {}
  } = e;
  const p = h(_);
  N(t, p, (r) => i(18, s = r));
  let {
    _internal: a = {}
  } = e, {
    label: g
  } = e, {
    form_name: S
  } = e, {
    as_item: I
  } = e, {
    visible: K = !0
  } = e, {
    elem_id: P = ""
  } = e, {
    elem_classes: v = []
  } = e, {
    elem_style: j = {}
  } = e;
  const [q, B] = ee({
    gradio: f,
    props: s,
    _internal: a,
    visible: K,
    elem_id: P,
    elem_classes: v,
    elem_style: j,
    as_item: I,
    label: g,
    form_name: S
  });
  N(t, q, (r) => i(0, o = r));
  const F = W();
  N(t, F, (r) => i(1, n = r));
  const {
    rules: x
  } = ce(["rules"]);
  return N(t, x, (r) => i(2, l = r)), t.$$set = (r) => {
    "gradio" in r && i(8, f = r.gradio), "props" in r && i(9, _ = r.props), "_internal" in r && i(10, a = r._internal), "label" in r && i(11, g = r.label), "form_name" in r && i(12, S = r.form_name), "as_item" in r && i(13, I = r.as_item), "visible" in r && i(14, K = r.visible), "elem_id" in r && i(15, P = r.elem_id), "elem_classes" in r && i(16, v = r.elem_classes), "elem_style" in r && i(17, j = r.elem_style), "$$scope" in r && i(20, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    512 && p.update((r) => ({
      ...r,
      ..._
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, label, form_name*/
    523520 && B({
      gradio: f,
      props: s,
      _internal: a,
      visible: K,
      elem_id: P,
      elem_classes: v,
      elem_style: j,
      as_item: I,
      label: g,
      form_name: S
    });
  }, [o, n, l, m, p, q, F, x, f, _, a, g, S, I, K, P, v, j, s, u, c];
}
class Fe extends ae {
  constructor(e) {
    super(), Ce(this, e, Ee, ze, Se, {
      gradio: 8,
      props: 9,
      _internal: 10,
      label: 11,
      form_name: 12,
      as_item: 13,
      visible: 14,
      elem_id: 15,
      elem_classes: 16,
      elem_style: 17
    });
  }
  get gradio() {
    return this.$$.ctx[8];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
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
  get _internal() {
    return this.$$.ctx[10];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
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
  get form_name() {
    return this.$$.ctx[12];
  }
  set form_name(e) {
    this.$$set({
      form_name: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[13];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[14];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[15];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[16];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[17];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  Fe as I,
  Oe as g,
  h as w
};
