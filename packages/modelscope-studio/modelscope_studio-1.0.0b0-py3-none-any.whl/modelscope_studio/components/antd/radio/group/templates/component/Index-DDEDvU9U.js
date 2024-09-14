async function B() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(t) {
  return await B(), t().then((e) => e.default);
}
function V(t) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = t;
  return Object.keys(i).reduce((o, n) => {
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
        return e.dispatch(u.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: b,
          component: s
        });
      };
      if (c.length > 1) {
        let m = {
          ...s.props[c[0]] || {}
        };
        o[c[0]] = m;
        for (let a = 1; a < c.length - 1; a++) {
          const g = {
            ...s.props[c[a]] || {}
          };
          m[c[a]] = g, m = g;
        }
        const b = c[c.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, o;
      }
      const _ = c[0];
      o[`on${_.slice(0, 1).toUpperCase()}${_.slice(1)}`] = f;
    }
    return o;
  }, {});
}
function N() {
}
function J(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function Q(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return N;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(t) {
  let e;
  return Q(t, (i) => e = i)(), e;
}
const w = [];
function h(t, e = N) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(u) {
    if (J(t, u) && (t = u, i)) {
      const c = !w.length;
      for (const f of s)
        f[1](), w.push(f, t);
      if (c) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function n(u) {
    o(u(t));
  }
  function l(u, c = N) {
    const f = [u, c];
    return s.add(f), s.size === 1 && (i = e(o, n) || N), u(t), () => {
      s.delete(f), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: E
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const t = h({});
  return E(T, t);
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
  const s = z($), o = ((u = y(s)) == null ? void 0 : u.as_item) || t.as_item, n = s ? o ? y(s)[o] : y(s) : {}, l = h({
    ...t,
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
const R = "$$ms-gr-antd-slot-key";
function te() {
  E(R, h(void 0));
}
function ne() {
  return z(R);
}
const U = "$$ms-gr-antd-component-slot-context-key";
function se({
  slot: t,
  index: e,
  subIndex: i
}) {
  return E(U, {
    slotKey: h(t),
    slotIndex: h(e),
    subSlotIndex: h(i)
  });
}
function Oe() {
  return z(U);
}
function oe(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var X = {
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
})(X);
var ie = X.exports;
const A = /* @__PURE__ */ oe(ie), {
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
      o && (l ? o[l].update((f) => {
        const _ = [...f];
        return n.includes(l) ? _[u] = c : _[u] = void 0, _;
      }) : n.includes("default") && o.default.update((f) => {
        const _ = [...f];
        return _[u] = c, _;
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
} = ue("radio-group"), {
  SvelteComponent: ae,
  assign: fe,
  check_outros: _e,
  component_subscribe: j,
  create_component: me,
  create_slot: de,
  destroy_component: pe,
  detach: Y,
  empty: D,
  flush: p,
  get_all_dirty_from_scope: be,
  get_slot_changes: ge,
  get_spread_object: F,
  get_spread_update: he,
  group_outros: ye,
  handle_promise: we,
  init: Ce,
  insert: G,
  mount_component: ke,
  noop: d,
  safe_not_equal: ve,
  transition_in: C,
  transition_out: k,
  update_await_block_branch: Se,
  update_slot_base: Ke
} = window.__gradio__svelte__internal;
function M(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ne,
    then: Pe,
    catch: Ie,
    value: 22,
    blocks: [, , ,]
  };
  return we(
    /*AwaitedRadioGroup*/
    t[4],
    s
  ), {
    c() {
      e = D(), s.block.c();
    },
    m(o, n) {
      G(o, e, n), s.block.m(o, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, i = !0;
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
      o && Y(e), s.block.d(o), s.token = null, s = null;
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
function Pe(t) {
  let e, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[1].elem_style
      )
    },
    {
      className: A(
        /*$mergedProps*/
        t[1].elem_classes,
        "ms-gr-antd-radio-group"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[1].elem_id
      )
    },
    /*$mergedProps*/
    t[1].props,
    V(
      /*$mergedProps*/
      t[1]
    ),
    {
      value: (
        /*$mergedProps*/
        t[1].props.value ?? /*$mergedProps*/
        t[1].value
      )
    },
    {
      slots: (
        /*$slots*/
        t[2]
      )
    },
    {
      optionItems: (
        /*$options*/
        t[3]
      )
    },
    {
      onValueChange: (
        /*func*/
        t[19]
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
    o = fe(o, s[n]);
  return e = new /*RadioGroup*/
  t[22]({
    props: o
  }), {
    c() {
      me(e.$$.fragment);
    },
    m(n, l) {
      ke(e, n, l), i = !0;
    },
    p(n, l) {
      const u = l & /*$mergedProps, $slots, $options, value*/
      15 ? he(s, [l & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          n[1].elem_style
        )
      }, l & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          n[1].elem_classes,
          "ms-gr-antd-radio-group"
        )
      }, l & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          n[1].elem_id
        )
      }, l & /*$mergedProps*/
      2 && F(
        /*$mergedProps*/
        n[1].props
      ), l & /*$mergedProps*/
      2 && F(V(
        /*$mergedProps*/
        n[1]
      )), l & /*$mergedProps*/
      2 && {
        value: (
          /*$mergedProps*/
          n[1].props.value ?? /*$mergedProps*/
          n[1].value
        )
      }, l & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          n[2]
        )
      }, l & /*$options*/
      8 && {
        optionItems: (
          /*$options*/
          n[3]
        )
      }, l & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          n[19]
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
      pe(e, n);
    }
  };
}
function je(t) {
  let e;
  const i = (
    /*#slots*/
    t[18].default
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
        e ? ge(
          i,
          /*$$scope*/
          o[20],
          n,
          null
        ) : be(
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
    t[1].visible && M(t)
  );
  return {
    c() {
      s && s.c(), e = D();
    },
    m(o, n) {
      s && s.m(o, n), G(o, e, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[1].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      2 && C(s, 1)) : (s = M(o), s.c(), C(s, 1), s.m(e.parentNode, e)) : s && (ye(), k(s, 1, 1, () => {
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
      o && Y(e), s && s.d(o);
    }
  };
}
function Ee(t, e, i) {
  let s, o, n, l, {
    $$slots: u = {},
    $$scope: c
  } = e;
  const f = H(() => import("./radio.group-DyEom6UO.js"));
  let {
    gradio: _
  } = e, {
    props: m = {}
  } = e;
  const b = h(m);
  j(t, b, (r) => i(17, s = r));
  let {
    _internal: a = {}
  } = e, {
    value: g
  } = e, {
    as_item: v
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: I = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [O, L] = ee({
    gradio: _,
    props: s,
    _internal: a,
    visible: S,
    elem_id: K,
    elem_classes: I,
    elem_style: P,
    as_item: v,
    value: g
  });
  j(t, O, (r) => i(1, o = r));
  const q = W();
  j(t, q, (r) => i(2, n = r));
  const {
    options: x
  } = ce(["options"]);
  j(t, x, (r) => i(3, l = r));
  const Z = (r) => {
    i(0, g = r);
  };
  return t.$$set = (r) => {
    "gradio" in r && i(9, _ = r.gradio), "props" in r && i(10, m = r.props), "_internal" in r && i(11, a = r._internal), "value" in r && i(0, g = r.value), "as_item" in r && i(12, v = r.as_item), "visible" in r && i(13, S = r.visible), "elem_id" in r && i(14, K = r.elem_id), "elem_classes" in r && i(15, I = r.elem_classes), "elem_style" in r && i(16, P = r.elem_style), "$$scope" in r && i(20, c = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*props*/
    1024 && b.update((r) => ({
      ...r,
      ...m
    })), t.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    260609 && L({
      gradio: _,
      props: s,
      _internal: a,
      visible: S,
      elem_id: K,
      elem_classes: I,
      elem_style: P,
      as_item: v,
      value: g
    });
  }, [g, o, n, l, f, b, O, q, x, _, m, a, v, S, K, I, P, s, u, Z, c];
}
class xe extends ae {
  constructor(e) {
    super(), Ce(this, e, Ee, ze, ve, {
      gradio: 9,
      props: 10,
      _internal: 11,
      value: 0,
      as_item: 12,
      visible: 13,
      elem_id: 14,
      elem_classes: 15,
      elem_style: 16
    });
  }
  get gradio() {
    return this.$$.ctx[9];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), p();
  }
  get props() {
    return this.$$.ctx[10];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[11];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[12];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[13];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[14];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[15];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[16];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
export {
  xe as I,
  Oe as g,
  h as w
};
