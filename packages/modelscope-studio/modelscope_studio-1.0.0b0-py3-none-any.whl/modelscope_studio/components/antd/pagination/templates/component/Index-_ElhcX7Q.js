async function G() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function H(e) {
  return await G(), e().then((t) => t.default);
}
function q(e) {
  const {
    gradio: t,
    _internal: s,
    ...n
  } = e;
  return Object.keys(s).reduce((i, o) => {
    const u = o.match(/bind_(.+)_event/);
    if (u) {
      const l = u[1], r = l.split("_"), f = (..._) => {
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
        return t.dispatch(l.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: p,
          component: n
        });
      };
      if (r.length > 1) {
        let _ = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = _;
        for (let a = 1; a < r.length - 1; a++) {
          const g = {
            ...n.props[r[a]] || {}
          };
          _[r[a]] = g, _ = g;
        }
        const p = r[r.length - 1];
        return _[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = f, i;
      }
      const m = r[0];
      i[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = f;
    }
    return i;
  }, {});
}
function P() {
}
function J(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Q(e, ...t) {
  if (e == null) {
    for (const n of t)
      n(void 0);
    return P;
  }
  const s = e.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function y(e) {
  let t;
  return Q(e, (s) => t = s)(), t;
}
const w = [];
function h(e, t = P) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function i(l) {
    if (J(e, l) && (e = l, s)) {
      const r = !w.length;
      for (const f of n)
        f[1](), w.push(f, e);
      if (r) {
        for (let f = 0; f < w.length; f += 2)
          w[f][0](w[f + 1]);
        w.length = 0;
      }
    }
  }
  function o(l) {
    i(l(e));
  }
  function u(l, r = P) {
    const f = [l, r];
    return n.add(f), n.size === 1 && (s = t(i, o) || P), l(e), () => {
      n.delete(f), n.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: u
  };
}
const {
  getContext: N,
  setContext: I
} = window.__gradio__svelte__internal, T = "$$ms-gr-antd-slots-key";
function W() {
  const e = h({});
  return I(T, e);
}
const x = "$$ms-gr-antd-context-key";
function $(e) {
  var l;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = te(), s = ne({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((r) => {
    s.slotKey.set(r);
  }), ee();
  const n = N(x), i = ((l = y(n)) == null ? void 0 : l.as_item) || e.as_item, o = n ? i ? y(n)[i] : y(n) : {}, u = h({
    ...e,
    ...o
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: f
    } = y(u);
    f && (r = r[f]), u.update((m) => ({
      ...m,
      ...r
    }));
  }), [u, (r) => {
    const f = r.as_item ? y(n)[r.as_item] : y(n);
    return u.set({
      ...r,
      ...f
    });
  }]) : [u, (r) => {
    u.set(r);
  }];
}
const U = "$$ms-gr-antd-slot-key";
function ee() {
  I(U, h(void 0));
}
function te() {
  return N(U);
}
const X = "$$ms-gr-antd-component-slot-context-key";
function ne({
  slot: e,
  index: t,
  subIndex: s
}) {
  return I(X, {
    slotKey: h(e),
    slotIndex: h(t),
    subSlotIndex: h(s)
  });
}
function Pe() {
  return N(X);
}
function se(e) {
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
    function s() {
      for (var o = "", u = 0; u < arguments.length; u++) {
        var l = arguments[u];
        l && (o = i(o, n(l)));
      }
      return o;
    }
    function n(o) {
      if (typeof o == "string" || typeof o == "number")
        return o;
      if (typeof o != "object")
        return "";
      if (Array.isArray(o))
        return s.apply(null, o);
      if (o.toString !== Object.prototype.toString && !o.toString.toString().includes("[native code]"))
        return o.toString();
      var u = "";
      for (var l in o)
        t.call(o, l) && o[l] && (u = i(u, l));
      return u;
    }
    function i(o, u) {
      return u ? o ? o + " " + u : o + u : o;
    }
    e.exports ? (s.default = s, e.exports = s) : window.classNames = s;
  })();
})(Y);
var ie = Y.exports;
const A = /* @__PURE__ */ se(ie), {
  SvelteComponent: oe,
  assign: le,
  check_outros: re,
  component_subscribe: j,
  create_component: ue,
  create_slot: ce,
  destroy_component: ae,
  detach: D,
  empty: F,
  flush: b,
  get_all_dirty_from_scope: fe,
  get_slot_changes: _e,
  get_spread_object: V,
  get_spread_update: me,
  group_outros: de,
  handle_promise: pe,
  init: be,
  insert: L,
  mount_component: ge,
  noop: d,
  safe_not_equal: he,
  transition_in: k,
  transition_out: S,
  update_await_block_branch: ye,
  update_slot_base: we
} = window.__gradio__svelte__internal;
function R(e) {
  let t, s, n = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ce,
    then: Se,
    catch: ke,
    value: 20,
    blocks: [, , ,]
  };
  return pe(
    /*AwaitedPagination*/
    e[3],
    n
  ), {
    c() {
      t = F(), n.block.c();
    },
    m(i, o) {
      L(i, t, o), n.block.m(i, n.anchor = o), n.mount = () => t.parentNode, n.anchor = t, s = !0;
    },
    p(i, o) {
      e = i, ye(n, e, o);
    },
    i(i) {
      s || (k(n.block), s = !0);
    },
    o(i) {
      for (let o = 0; o < 3; o += 1) {
        const u = n.blocks[o];
        S(u);
      }
      s = !1;
    },
    d(i) {
      i && D(t), n.block.d(i), n.token = null, n = null;
    }
  };
}
function ke(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Se(e) {
  var o, u;
  let t, s;
  const n = [
    {
      style: (
        /*$mergedProps*/
        e[1].elem_style
      )
    },
    {
      className: A(
        /*$mergedProps*/
        e[1].elem_classes,
        "ms-gr-antd-pagination"
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
    q(
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
      current: (
        /*$mergedProps*/
        e[1].props.current || /*$mergedProps*/
        ((o = e[1].value) == null ? void 0 : o.page) || void 0
      )
    },
    {
      pageSize: (
        /*$mergedProps*/
        e[1].props.pageSize || /*$mergedProps*/
        ((u = e[1].value) == null ? void 0 : u.page_size) || void 0
      )
    },
    {
      onValueChange: (
        /*func*/
        e[17]
      )
    }
  ];
  let i = {
    $$slots: {
      default: [ve]
    },
    $$scope: {
      ctx: e
    }
  };
  for (let l = 0; l < n.length; l += 1)
    i = le(i, n[l]);
  return t = new /*Pagination*/
  e[20]({
    props: i
  }), {
    c() {
      ue(t.$$.fragment);
    },
    m(l, r) {
      ge(t, l, r), s = !0;
    },
    p(l, r) {
      var m, _;
      const f = r & /*$mergedProps, $slots, undefined, value*/
      7 ? me(n, [r & /*$mergedProps*/
      2 && {
        style: (
          /*$mergedProps*/
          l[1].elem_style
        )
      }, r & /*$mergedProps*/
      2 && {
        className: A(
          /*$mergedProps*/
          l[1].elem_classes,
          "ms-gr-antd-pagination"
        )
      }, r & /*$mergedProps*/
      2 && {
        id: (
          /*$mergedProps*/
          l[1].elem_id
        )
      }, r & /*$mergedProps*/
      2 && V(
        /*$mergedProps*/
        l[1].props
      ), r & /*$mergedProps*/
      2 && V(q(
        /*$mergedProps*/
        l[1]
      )), r & /*$slots*/
      4 && {
        slots: (
          /*$slots*/
          l[2]
        )
      }, r & /*$mergedProps, undefined*/
      2 && {
        current: (
          /*$mergedProps*/
          l[1].props.current || /*$mergedProps*/
          ((m = l[1].value) == null ? void 0 : m.page) || void 0
        )
      }, r & /*$mergedProps, undefined*/
      2 && {
        pageSize: (
          /*$mergedProps*/
          l[1].props.pageSize || /*$mergedProps*/
          ((_ = l[1].value) == null ? void 0 : _.page_size) || void 0
        )
      }, r & /*value*/
      1 && {
        onValueChange: (
          /*func*/
          l[17]
        )
      }]) : {};
      r & /*$$scope*/
      262144 && (f.$$scope = {
        dirty: r,
        ctx: l
      }), t.$set(f);
    },
    i(l) {
      s || (k(t.$$.fragment, l), s = !0);
    },
    o(l) {
      S(t.$$.fragment, l), s = !1;
    },
    d(l) {
      ae(t, l);
    }
  };
}
function ve(e) {
  let t;
  const s = (
    /*#slots*/
    e[16].default
  ), n = ce(
    s,
    e,
    /*$$scope*/
    e[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, o) {
      n && n.m(i, o), t = !0;
    },
    p(i, o) {
      n && n.p && (!t || o & /*$$scope*/
      262144) && we(
        n,
        s,
        i,
        /*$$scope*/
        i[18],
        t ? _e(
          s,
          /*$$scope*/
          i[18],
          o,
          null
        ) : fe(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      t || (k(n, i), t = !0);
    },
    o(i) {
      S(n, i), t = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function Ce(e) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function Ke(e) {
  let t, s, n = (
    /*$mergedProps*/
    e[1].visible && R(e)
  );
  return {
    c() {
      n && n.c(), t = F();
    },
    m(i, o) {
      n && n.m(i, o), L(i, t, o), s = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, o), o & /*$mergedProps*/
      2 && k(n, 1)) : (n = R(i), n.c(), k(n, 1), n.m(t.parentNode, t)) : n && (de(), S(n, 1, 1, () => {
        n = null;
      }), re());
    },
    i(i) {
      s || (k(n), s = !0);
    },
    o(i) {
      S(n), s = !1;
    },
    d(i) {
      i && D(t), n && n.d(i);
    }
  };
}
function ze(e, t, s) {
  let n, i, o, {
    $$slots: u = {},
    $$scope: l
  } = t;
  const r = H(() => import("./pagination-COzs_c2t.js"));
  let {
    gradio: f
  } = t, {
    props: m = {}
  } = t;
  const _ = h(m);
  j(e, _, (c) => s(15, n = c));
  let {
    _internal: p = {}
  } = t, {
    value: a = {}
  } = t, {
    as_item: g
  } = t, {
    visible: v = !0
  } = t, {
    elem_id: C = ""
  } = t, {
    elem_classes: K = []
  } = t, {
    elem_style: z = {}
  } = t;
  const [E, M] = $({
    gradio: f,
    props: n,
    _internal: p,
    visible: v,
    elem_id: C,
    elem_classes: K,
    elem_style: z,
    as_item: g,
    value: a
  });
  j(e, E, (c) => s(1, i = c));
  const O = W();
  j(e, O, (c) => s(2, o = c));
  const Z = (c, B) => {
    s(0, a = {
      page: c,
      page_size: B
    });
  };
  return e.$$set = (c) => {
    "gradio" in c && s(7, f = c.gradio), "props" in c && s(8, m = c.props), "_internal" in c && s(9, p = c._internal), "value" in c && s(0, a = c.value), "as_item" in c && s(10, g = c.as_item), "visible" in c && s(11, v = c.visible), "elem_id" in c && s(12, C = c.elem_id), "elem_classes" in c && s(13, K = c.elem_classes), "elem_style" in c && s(14, z = c.elem_style), "$$scope" in c && s(18, l = c.$$scope);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    256 && _.update((c) => ({
      ...c,
      ...m
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65153 && M({
      gradio: f,
      props: n,
      _internal: p,
      visible: v,
      elem_id: C,
      elem_classes: K,
      elem_style: z,
      as_item: g,
      value: a
    });
  }, [a, i, o, r, _, E, O, f, m, p, g, v, C, K, z, n, u, Z, l];
}
class je extends oe {
  constructor(t) {
    super(), be(this, t, ze, Ke, he, {
      gradio: 7,
      props: 8,
      _internal: 9,
      value: 0,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[7];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[8];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[9];
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
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  je as I,
  Pe as g,
  h as w
};
