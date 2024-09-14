function $(n) {
  const {
    gradio: t,
    _internal: s,
    ...e
  } = n;
  return Object.keys(s).reduce((r, i) => {
    const o = i.match(/bind_(.+)_event/);
    if (o) {
      const c = o[1], u = c.split("_"), f = (...a) => {
        const x = a.map((_) => a && typeof _ == "object" && (_.nativeEvent || _ instanceof Event) ? {
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
        return t.dispatch(c.replace(/[A-Z]/g, (_) => "_" + _.toLowerCase()), {
          payload: x,
          component: e
        });
      };
      if (u.length > 1) {
        let a = {
          ...e.props[u[0]] || {}
        };
        r[u[0]] = a;
        for (let _ = 1; _ < u.length - 1; _++) {
          const g = {
            ...e.props[u[_]] || {}
          };
          a[u[_]] = g, a = g;
        }
        const x = u[u.length - 1];
        return a[`on${x.slice(0, 1).toUpperCase()}${x.slice(1)}`] = f, r;
      }
      const d = u[0];
      r[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = f;
    }
    return r;
  }, {});
}
function V() {
}
function tt(n, t) {
  return n != n ? t == t : n !== t || n && typeof n == "object" || typeof n == "function";
}
function et(n, ...t) {
  if (n == null) {
    for (const e of t)
      e(void 0);
    return V;
  }
  const s = n.subscribe(...t);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function b(n) {
  let t;
  return et(n, (s) => t = s)(), t;
}
const y = [];
function h(n, t = V) {
  let s;
  const e = /* @__PURE__ */ new Set();
  function r(c) {
    if (tt(n, c) && (n = c, s)) {
      const u = !y.length;
      for (const f of e)
        f[1](), y.push(f, n);
      if (u) {
        for (let f = 0; f < y.length; f += 2)
          y[f][0](y[f + 1]);
        y.length = 0;
      }
    }
  }
  function i(c) {
    r(c(n));
  }
  function o(c, u = V) {
    const f = [c, u];
    return e.add(f), e.size === 1 && (s = t(r, i) || V), c(n), () => {
      e.delete(f), e.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: r,
    update: i,
    subscribe: o
  };
}
const {
  getContext: L,
  setContext: Z
} = window.__gradio__svelte__internal, st = "$$ms-gr-antd-context-key";
function nt(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = G(), s = rt({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  t && t.subscribe((u) => {
    s.slotKey.set(u);
  }), it();
  const e = L(st), r = ((c = b(e)) == null ? void 0 : c.as_item) || n.as_item, i = e ? r ? b(e)[r] : b(e) : {}, o = h({
    ...n,
    ...i
  });
  return e ? (e.subscribe((u) => {
    const {
      as_item: f
    } = b(o);
    f && (u = u[f]), o.update((d) => ({
      ...d,
      ...u
    }));
  }), [o, (u) => {
    const f = u.as_item ? b(e)[u.as_item] : b(e);
    return o.set({
      ...u,
      ...f
    });
  }]) : [o, (u) => {
    o.set(u);
  }];
}
const B = "$$ms-gr-antd-slot-key";
function it() {
  Z(B, h(void 0));
}
function G() {
  return L(B);
}
const lt = "$$ms-gr-antd-component-slot-context-key";
function rt({
  slot: n,
  index: t,
  subIndex: s
}) {
  return Z(lt, {
    slotKey: h(n),
    slotIndex: h(t),
    subSlotIndex: h(s)
  });
}
function ot(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var H = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var t = {}.hasOwnProperty;
    function s() {
      for (var i = "", o = 0; o < arguments.length; o++) {
        var c = arguments[o];
        c && (i = r(i, e(c)));
      }
      return i;
    }
    function e(i) {
      if (typeof i == "string" || typeof i == "number")
        return i;
      if (typeof i != "object")
        return "";
      if (Array.isArray(i))
        return s.apply(null, i);
      if (i.toString !== Object.prototype.toString && !i.toString.toString().includes("[native code]"))
        return i.toString();
      var o = "";
      for (var c in i)
        t.call(i, c) && i[c] && (o = r(o, c));
      return o;
    }
    function r(i, o) {
      return o ? i ? i + " " + o : i + o : i;
    }
    n.exports ? (s.default = s, n.exports = s) : window.classNames = s;
  })();
})(H);
var ut = H.exports;
const ct = /* @__PURE__ */ ot(ut), {
  getContext: ft,
  setContext: _t
} = window.__gradio__svelte__internal;
function mt(n) {
  const t = `$$ms-gr-antd-${n}-context-key`;
  function s(r = ["default"]) {
    const i = r.reduce((o, c) => (o[c] = h([]), o), {});
    return _t(t, {
      itemsMap: i,
      allowedSlots: r
    }), i;
  }
  function e() {
    const {
      itemsMap: r,
      allowedSlots: i
    } = ft(t);
    return function(o, c, u) {
      r && (o ? r[o].update((f) => {
        const d = [...f];
        return i.includes(o) ? d[c] = u : d[c] = void 0, d;
      }) : i.includes("default") && r.default.update((f) => {
        const d = [...f];
        return d[c] = u, d;
      }));
    };
  }
  return {
    getItems: s,
    getSetItemFn: e
  };
}
const {
  getItems: Et,
  getSetItemFn: dt
} = mt("grid"), {
  SvelteComponent: at,
  binding_callbacks: xt,
  check_outros: ht,
  component_subscribe: M,
  create_slot: gt,
  detach: J,
  element: bt,
  empty: yt,
  flush: m,
  get_all_dirty_from_scope: Ct,
  get_slot_changes: Kt,
  group_outros: St,
  init: wt,
  insert: Q,
  safe_not_equal: It,
  set_custom_element_data: kt,
  transition_in: v,
  transition_out: U,
  update_slot_base: jt
} = window.__gradio__svelte__internal;
function D(n) {
  let t, s;
  const e = (
    /*#slots*/
    n[29].default
  ), r = gt(
    e,
    n,
    /*$$scope*/
    n[28],
    null
  );
  return {
    c() {
      t = bt("svelte-slot"), r && r.c(), kt(t, "class", "svelte-1y8zqvi");
    },
    m(i, o) {
      Q(i, t, o), r && r.m(t, null), n[30](t), s = !0;
    },
    p(i, o) {
      r && r.p && (!s || o[0] & /*$$scope*/
      268435456) && jt(
        r,
        e,
        i,
        /*$$scope*/
        i[28],
        s ? Kt(
          e,
          /*$$scope*/
          i[28],
          o,
          null
        ) : Ct(
          /*$$scope*/
          i[28]
        ),
        null
      );
    },
    i(i) {
      s || (v(r, i), s = !0);
    },
    o(i) {
      U(r, i), s = !1;
    },
    d(i) {
      i && J(t), r && r.d(i), n[30](null);
    }
  };
}
function Pt(n) {
  let t, s, e = (
    /*$mergedProps*/
    n[0].visible && D(n)
  );
  return {
    c() {
      e && e.c(), t = yt();
    },
    m(r, i) {
      e && e.m(r, i), Q(r, t, i), s = !0;
    },
    p(r, i) {
      /*$mergedProps*/
      r[0].visible ? e ? (e.p(r, i), i[0] & /*$mergedProps*/
      1 && v(e, 1)) : (e = D(r), e.c(), v(e, 1), e.m(t.parentNode, t)) : e && (St(), U(e, 1, 1, () => {
        e = null;
      }), ht());
    },
    i(r) {
      s || (v(e), s = !0);
    },
    o(r) {
      U(e), s = !1;
    },
    d(r) {
      r && J(t), e && e.d(r);
    }
  };
}
function qt(n, t, s) {
  let e, r, i, o, {
    $$slots: c = {},
    $$scope: u
  } = t, {
    gradio: f
  } = t, {
    props: d = {}
  } = t;
  const a = h(d);
  M(n, a, (l) => s(27, o = l));
  let {
    _internal: x = {}
  } = t, {
    flex: _
  } = t, {
    offset: g
  } = t, {
    order: C
  } = t, {
    pull: K
  } = t, {
    push: S
  } = t, {
    span: w
  } = t, {
    xs: I
  } = t, {
    sm: k
  } = t, {
    md: j
  } = t, {
    lg: P
  } = t, {
    xl: q
  } = t, {
    xxl: E
  } = t, {
    as_item: N
  } = t, {
    visible: O = !0
  } = t, {
    elem_id: z = ""
  } = t, {
    elem_classes: A = []
  } = t, {
    elem_style: F = {}
  } = t;
  const X = G();
  M(n, X, (l) => s(26, i = l));
  const [Y, T] = nt({
    gradio: f,
    props: o,
    _internal: x,
    visible: O,
    elem_id: z,
    elem_classes: A,
    elem_style: F,
    as_item: N,
    flex: _,
    offset: g,
    order: C,
    pull: K,
    push: S,
    span: w,
    xs: I,
    sm: k,
    md: j,
    lg: P,
    xl: q,
    xxl: E
  });
  M(n, Y, (l) => s(0, e = l));
  const R = h();
  M(n, R, (l) => s(1, r = l));
  const W = dt();
  function p(l) {
    xt[l ? "unshift" : "push"](() => {
      r = l, R.set(r);
    });
  }
  return n.$$set = (l) => {
    "gradio" in l && s(6, f = l.gradio), "props" in l && s(7, d = l.props), "_internal" in l && s(8, x = l._internal), "flex" in l && s(9, _ = l.flex), "offset" in l && s(10, g = l.offset), "order" in l && s(11, C = l.order), "pull" in l && s(12, K = l.pull), "push" in l && s(13, S = l.push), "span" in l && s(14, w = l.span), "xs" in l && s(15, I = l.xs), "sm" in l && s(16, k = l.sm), "md" in l && s(17, j = l.md), "lg" in l && s(18, P = l.lg), "xl" in l && s(19, q = l.xl), "xxl" in l && s(20, E = l.xxl), "as_item" in l && s(21, N = l.as_item), "visible" in l && s(22, O = l.visible), "elem_id" in l && s(23, z = l.elem_id), "elem_classes" in l && s(24, A = l.elem_classes), "elem_style" in l && s(25, F = l.elem_style), "$$scope" in l && s(28, u = l.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*props*/
    128 && a.update((l) => ({
      ...l,
      ...d
    })), n.$$.dirty[0] & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, flex, offset, order, pull, push, span, xs, sm, md, lg, xl, xxl*/
    201326400 && T({
      gradio: f,
      props: o,
      _internal: x,
      visible: O,
      elem_id: z,
      elem_classes: A,
      elem_style: F,
      as_item: N,
      flex: _,
      offset: g,
      order: C,
      pull: K,
      push: S,
      span: w,
      xs: I,
      sm: k,
      md: j,
      lg: P,
      xl: q,
      xxl: E
    }), n.$$.dirty[0] & /*$slot, $slotKey, $mergedProps*/
    67108867 && r && W(i, e._internal.index || 0, {
      el: r,
      props: {
        style: e.elem_style,
        className: ct(e.elem_classes, "ms-gr-antd-col"),
        id: e.elem_id,
        flex: e.flex,
        offset: e.offset,
        order: e.order,
        pull: e.pull,
        push: e.push,
        span: e.span,
        xs: e.xs,
        sm: e.sm,
        md: e.md,
        lg: e.lg,
        xl: e.xl,
        xxl: e.xxl,
        ...e.props,
        ...$(e)
      },
      slots: {}
    });
  }, [e, r, a, X, Y, R, f, d, x, _, g, C, K, S, w, I, k, j, P, q, E, N, O, z, A, F, i, o, u, c, p];
}
class Nt extends at {
  constructor(t) {
    super(), wt(this, t, qt, Pt, It, {
      gradio: 6,
      props: 7,
      _internal: 8,
      flex: 9,
      offset: 10,
      order: 11,
      pull: 12,
      push: 13,
      span: 14,
      xs: 15,
      sm: 16,
      md: 17,
      lg: 18,
      xl: 19,
      xxl: 20,
      as_item: 21,
      visible: 22,
      elem_id: 23,
      elem_classes: 24,
      elem_style: 25
    }, null, [-1, -1]);
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), m();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), m();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), m();
  }
  get flex() {
    return this.$$.ctx[9];
  }
  set flex(t) {
    this.$$set({
      flex: t
    }), m();
  }
  get offset() {
    return this.$$.ctx[10];
  }
  set offset(t) {
    this.$$set({
      offset: t
    }), m();
  }
  get order() {
    return this.$$.ctx[11];
  }
  set order(t) {
    this.$$set({
      order: t
    }), m();
  }
  get pull() {
    return this.$$.ctx[12];
  }
  set pull(t) {
    this.$$set({
      pull: t
    }), m();
  }
  get push() {
    return this.$$.ctx[13];
  }
  set push(t) {
    this.$$set({
      push: t
    }), m();
  }
  get span() {
    return this.$$.ctx[14];
  }
  set span(t) {
    this.$$set({
      span: t
    }), m();
  }
  get xs() {
    return this.$$.ctx[15];
  }
  set xs(t) {
    this.$$set({
      xs: t
    }), m();
  }
  get sm() {
    return this.$$.ctx[16];
  }
  set sm(t) {
    this.$$set({
      sm: t
    }), m();
  }
  get md() {
    return this.$$.ctx[17];
  }
  set md(t) {
    this.$$set({
      md: t
    }), m();
  }
  get lg() {
    return this.$$.ctx[18];
  }
  set lg(t) {
    this.$$set({
      lg: t
    }), m();
  }
  get xl() {
    return this.$$.ctx[19];
  }
  set xl(t) {
    this.$$set({
      xl: t
    }), m();
  }
  get xxl() {
    return this.$$.ctx[20];
  }
  set xxl(t) {
    this.$$set({
      xxl: t
    }), m();
  }
  get as_item() {
    return this.$$.ctx[21];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), m();
  }
  get visible() {
    return this.$$.ctx[22];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), m();
  }
  get elem_id() {
    return this.$$.ctx[23];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), m();
  }
  get elem_classes() {
    return this.$$.ctx[24];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), m();
  }
  get elem_style() {
    return this.$$.ctx[25];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), m();
  }
}
export {
  Nt as default
};
