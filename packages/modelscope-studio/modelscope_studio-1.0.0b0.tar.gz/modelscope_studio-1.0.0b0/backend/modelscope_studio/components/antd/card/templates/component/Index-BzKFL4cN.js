async function re() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((t) => {
    window.ms_globals.initialize = () => {
      t();
    };
  })), await window.ms_globals.initializePromise;
}
async function oe(t) {
  return await re(), t().then((e) => e.default);
}
function Z(t) {
  const {
    gradio: e,
    _internal: i,
    ...s
  } = t;
  return Object.keys(i).reduce((l, n) => {
    const r = n.match(/bind_(.+)_event/);
    if (r) {
      const _ = r[1], a = _.split("_"), u = (...b) => {
        const h = b.map((c) => b && typeof c == "object" && (c.nativeEvent || c instanceof Event) ? {
          type: c.type,
          detail: c.detail,
          timestamp: c.timeStamp,
          clientX: c.clientX,
          clientY: c.clientY,
          targetId: c.target.id,
          targetClassName: c.target.className,
          altKey: c.altKey,
          ctrlKey: c.ctrlKey,
          shiftKey: c.shiftKey,
          metaKey: c.metaKey
        } : c);
        return e.dispatch(_.replace(/[A-Z]/g, (c) => "_" + c.toLowerCase()), {
          payload: h,
          component: s
        });
      };
      if (a.length > 1) {
        let b = {
          ...s.props[a[0]] || {}
        };
        l[a[0]] = b;
        for (let c = 1; c < a.length - 1; c++) {
          const m = {
            ...s.props[a[c]] || {}
          };
          b[a[c]] = m, b = m;
        }
        const h = a[a.length - 1];
        return b[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = u, l;
      }
      const d = a[0];
      l[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = u;
    }
    return l;
  }, {});
}
function K() {
}
function ae(t) {
  return t();
}
function ce(t) {
  t.forEach(ae);
}
function _e(t) {
  return typeof t == "function";
}
function ue(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function W(t, ...e) {
  if (t == null) {
    for (const s of e)
      s(void 0);
    return K;
  }
  const i = t.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function w(t) {
  let e;
  return W(t, (i) => e = i)(), e;
}
const C = [];
function fe(t, e) {
  return {
    subscribe: v(t, e).subscribe
  };
}
function v(t, e = K) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function l(_) {
    if (ue(t, _) && (t = _, i)) {
      const a = !C.length;
      for (const u of s)
        u[1](), C.push(u, t);
      if (a) {
        for (let u = 0; u < C.length; u += 2)
          C[u][0](C[u + 1]);
        C.length = 0;
      }
    }
  }
  function n(_) {
    l(_(t));
  }
  function r(_, a = K) {
    const u = [_, a];
    return s.add(u), s.size === 1 && (i = e(l, n) || K), _(t), () => {
      s.delete(u), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: l,
    update: n,
    subscribe: r
  };
}
function De(t, e, i) {
  const s = !Array.isArray(t), l = s ? [t] : t;
  if (!l.every(Boolean))
    throw new Error("derived() expects stores as input, got a falsy value");
  const n = e.length < 2;
  return fe(i, (r, _) => {
    let a = !1;
    const u = [];
    let d = 0, b = K;
    const h = () => {
      if (d)
        return;
      b();
      const m = e(s ? u[0] : u, r, _);
      n ? r(m) : b = _e(m) ? m : K;
    }, c = l.map((m, y) => W(m, (k) => {
      u[y] = k, d &= ~(1 << y), a && h();
    }, () => {
      d |= 1 << y;
    }));
    return a = !0, h(), function() {
      ce(c), b(), a = !1;
    };
  });
}
const {
  getContext: D,
  setContext: F
} = window.__gradio__svelte__internal, be = "$$ms-gr-antd-slots-key";
function me() {
  const t = v({});
  return F(be, t);
}
const de = "$$ms-gr-antd-context-key";
function he(t) {
  var _;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = ye(), i = ve({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((a) => {
    i.slotKey.set(a);
  }), ge();
  const s = D(de), l = ((_ = w(s)) == null ? void 0 : _.as_item) || t.as_item, n = s ? l ? w(s)[l] : w(s) : {}, r = v({
    ...t,
    ...n
  });
  return s ? (s.subscribe((a) => {
    const {
      as_item: u
    } = w(r);
    u && (a = a[u]), r.update((d) => ({
      ...d,
      ...a
    }));
  }), [r, (a) => {
    const u = a.as_item ? w(s)[a.as_item] : w(s);
    return r.set({
      ...a,
      ...u
    });
  }]) : [r, (a) => {
    r.set(a);
  }];
}
const $ = "$$ms-gr-antd-slot-key";
function ge() {
  F($, v(void 0));
}
function ye() {
  return D($);
}
const ee = "$$ms-gr-antd-component-slot-context-key";
function ve({
  slot: t,
  index: e,
  subIndex: i
}) {
  return F(ee, {
    slotKey: v(t),
    slotIndex: v(e),
    subSlotIndex: v(i)
  });
}
function Fe() {
  return D(ee);
}
function ke(t) {
  return t && t.__esModule && Object.prototype.hasOwnProperty.call(t, "default") ? t.default : t;
}
var te = {
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
      for (var n = "", r = 0; r < arguments.length; r++) {
        var _ = arguments[r];
        _ && (n = l(n, s(_)));
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
      var r = "";
      for (var _ in n)
        e.call(n, _) && n[_] && (r = l(r, _));
      return r;
    }
    function l(n, r) {
      return r ? n ? n + " " + r : n + r : n;
    }
    t.exports ? (i.default = i, t.exports = i) : window.classNames = i;
  })();
})(te);
var we = te.exports;
const H = /* @__PURE__ */ ke(we), {
  SvelteComponent: Ce,
  assign: Ke,
  check_outros: ze,
  component_subscribe: Y,
  create_component: Se,
  create_slot: Pe,
  destroy_component: xe,
  detach: ne,
  empty: se,
  flush: f,
  get_all_dirty_from_scope: Ee,
  get_slot_changes: Ne,
  get_spread_object: J,
  get_spread_update: je,
  group_outros: Ae,
  handle_promise: Ie,
  init: pe,
  insert: ie,
  mount_component: Oe,
  noop: g,
  safe_not_equal: qe,
  transition_in: z,
  transition_out: S,
  update_await_block_branch: Te,
  update_slot_base: Be
} = window.__gradio__svelte__internal;
function Q(t) {
  let e, i, s = {
    ctx: t,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Ue,
    then: Ge,
    catch: Le,
    value: 34,
    blocks: [, , ,]
  };
  return Ie(
    /*AwaitedCard*/
    t[2],
    s
  ), {
    c() {
      e = se(), s.block.c();
    },
    m(l, n) {
      ie(l, e, n), s.block.m(l, s.anchor = n), s.mount = () => e.parentNode, s.anchor = e, i = !0;
    },
    p(l, n) {
      t = l, Te(s, t, n);
    },
    i(l) {
      i || (z(s.block), i = !0);
    },
    o(l) {
      for (let n = 0; n < 3; n += 1) {
        const r = s.blocks[n];
        S(r);
      }
      i = !1;
    },
    d(l) {
      l && ne(e), s.block.d(l), s.token = null, s = null;
    }
  };
}
function Le(t) {
  return {
    c: g,
    m: g,
    p: g,
    i: g,
    o: g,
    d: g
  };
}
function Ge(t) {
  let e, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        t[0].elem_style
      )
    },
    {
      className: H(
        /*$mergedProps*/
        t[0].elem_classes,
        "ms-gr-antd-card"
      )
    },
    {
      id: (
        /*$mergedProps*/
        t[0].elem_id
      )
    },
    {
      actions: (
        /*$mergedProps*/
        t[0].actions
      )
    },
    {
      activeTabKey: (
        /*$mergedProps*/
        t[0].active_tab_key
      )
    },
    {
      bordered: (
        /*$mergedProps*/
        t[0].bordered
      )
    },
    {
      cover: (
        /*$mergedProps*/
        t[0].cover
      )
    },
    {
      defaultActiveTabKey: (
        /*$mergedProps*/
        t[0].default_active_tab_key
      )
    },
    {
      extra: (
        /*$mergedProps*/
        t[0].extra
      )
    },
    {
      hoverable: (
        /*$mergedProps*/
        t[0].hoverable
      )
    },
    {
      loading: (
        /*$mergedProps*/
        t[0].loading
      )
    },
    {
      size: (
        /*$mergedProps*/
        t[0].size
      )
    },
    {
      tabBarExtraContent: (
        /*$mergedProps*/
        t[0].tab_bar_extra_content
      )
    },
    {
      tabList: (
        /*$mergedProps*/
        t[0].tab_list
      )
    },
    {
      tabProps: (
        /*$mergedProps*/
        t[0].tab_props
      )
    },
    {
      title: (
        /*$mergedProps*/
        t[0].title
      )
    },
    {
      type: (
        /*$mergedProps*/
        t[0].type
      )
    },
    {
      classNames: (
        /*$mergedProps*/
        t[0].class_names
      )
    },
    {
      styles: (
        /*$mergedProps*/
        t[0].styles
      )
    },
    /*$mergedProps*/
    t[0].props,
    Z(
      /*$mergedProps*/
      t[0]
    ),
    {
      containsGrid: (
        /*$mergedProps*/
        t[0]._internal.contains_grid
      )
    },
    {
      slots: (
        /*$slots*/
        t[1]
      )
    }
  ];
  let l = {
    $$slots: {
      default: [Re]
    },
    $$scope: {
      ctx: t
    }
  };
  for (let n = 0; n < s.length; n += 1)
    l = Ke(l, s[n]);
  return e = new /*Card*/
  t[34]({
    props: l
  }), {
    c() {
      Se(e.$$.fragment);
    },
    m(n, r) {
      Oe(e, n, r), i = !0;
    },
    p(n, r) {
      const _ = r[0] & /*$mergedProps, $slots*/
      3 ? je(s, [r[0] & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        className: H(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-card"
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        actions: (
          /*$mergedProps*/
          n[0].actions
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        activeTabKey: (
          /*$mergedProps*/
          n[0].active_tab_key
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        bordered: (
          /*$mergedProps*/
          n[0].bordered
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        cover: (
          /*$mergedProps*/
          n[0].cover
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        defaultActiveTabKey: (
          /*$mergedProps*/
          n[0].default_active_tab_key
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        extra: (
          /*$mergedProps*/
          n[0].extra
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        hoverable: (
          /*$mergedProps*/
          n[0].hoverable
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        loading: (
          /*$mergedProps*/
          n[0].loading
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        size: (
          /*$mergedProps*/
          n[0].size
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        tabBarExtraContent: (
          /*$mergedProps*/
          n[0].tab_bar_extra_content
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        tabList: (
          /*$mergedProps*/
          n[0].tab_list
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        tabProps: (
          /*$mergedProps*/
          n[0].tab_props
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        title: (
          /*$mergedProps*/
          n[0].title
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        type: (
          /*$mergedProps*/
          n[0].type
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        classNames: (
          /*$mergedProps*/
          n[0].class_names
        )
      }, r[0] & /*$mergedProps*/
      1 && {
        styles: (
          /*$mergedProps*/
          n[0].styles
        )
      }, r[0] & /*$mergedProps*/
      1 && J(
        /*$mergedProps*/
        n[0].props
      ), r[0] & /*$mergedProps*/
      1 && J(Z(
        /*$mergedProps*/
        n[0]
      )), r[0] & /*$mergedProps*/
      1 && {
        containsGrid: (
          /*$mergedProps*/
          n[0]._internal.contains_grid
        )
      }, r[0] & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }]) : {};
      r[1] & /*$$scope*/
      2 && (_.$$scope = {
        dirty: r,
        ctx: n
      }), e.$set(_);
    },
    i(n) {
      i || (z(e.$$.fragment, n), i = !0);
    },
    o(n) {
      S(e.$$.fragment, n), i = !1;
    },
    d(n) {
      xe(e, n);
    }
  };
}
function Re(t) {
  let e;
  const i = (
    /*#slots*/
    t[31].default
  ), s = Pe(
    i,
    t,
    /*$$scope*/
    t[32],
    null
  );
  return {
    c() {
      s && s.c();
    },
    m(l, n) {
      s && s.m(l, n), e = !0;
    },
    p(l, n) {
      s && s.p && (!e || n[1] & /*$$scope*/
      2) && Be(
        s,
        i,
        l,
        /*$$scope*/
        l[32],
        e ? Ne(
          i,
          /*$$scope*/
          l[32],
          n,
          null
        ) : Ee(
          /*$$scope*/
          l[32]
        ),
        null
      );
    },
    i(l) {
      e || (z(s, l), e = !0);
    },
    o(l) {
      S(s, l), e = !1;
    },
    d(l) {
      s && s.d(l);
    }
  };
}
function Ue(t) {
  return {
    c: g,
    m: g,
    p: g,
    i: g,
    o: g,
    d: g
  };
}
function Xe(t) {
  let e, i, s = (
    /*$mergedProps*/
    t[0].visible && Q(t)
  );
  return {
    c() {
      s && s.c(), e = se();
    },
    m(l, n) {
      s && s.m(l, n), ie(l, e, n), i = !0;
    },
    p(l, n) {
      /*$mergedProps*/
      l[0].visible ? s ? (s.p(l, n), n[0] & /*$mergedProps*/
      1 && z(s, 1)) : (s = Q(l), s.c(), z(s, 1), s.m(e.parentNode, e)) : s && (Ae(), S(s, 1, 1, () => {
        s = null;
      }), ze());
    },
    i(l) {
      i || (z(s), i = !0);
    },
    o(l) {
      S(s), i = !1;
    },
    d(l) {
      l && ne(e), s && s.d(l);
    }
  };
}
function Ye(t, e, i) {
  let s, l, n, {
    $$slots: r = {},
    $$scope: _
  } = e;
  const a = oe(() => import("./card-CN7wvYck.js"));
  let {
    gradio: u
  } = e, {
    _internal: d = {}
  } = e, {
    actions: b
  } = e, {
    active_tab_key: h
  } = e, {
    bordered: c
  } = e, {
    cover: m
  } = e, {
    default_active_tab_key: y
  } = e, {
    extra: k
  } = e, {
    hoverable: P
  } = e, {
    loading: x
  } = e, {
    size: E
  } = e, {
    tab_bar_extra_content: N
  } = e, {
    tab_list: j
  } = e, {
    tab_props: A
  } = e, {
    title: I
  } = e, {
    type: p
  } = e, {
    class_names: O
  } = e, {
    styles: q
  } = e, {
    as_item: T
  } = e, {
    props: B = {}
  } = e;
  const X = v(B);
  Y(t, X, (o) => i(30, s = o));
  let {
    elem_id: L = ""
  } = e, {
    elem_classes: G = []
  } = e, {
    elem_style: R = {}
  } = e, {
    visible: U = !0
  } = e;
  const M = me();
  Y(t, M, (o) => i(1, n = o));
  const [V, le] = he({
    gradio: u,
    props: s,
    _internal: d,
    as_item: T,
    visible: U,
    elem_id: L,
    elem_classes: G,
    elem_style: R,
    actions: b,
    active_tab_key: h,
    bordered: c,
    cover: m,
    default_active_tab_key: y,
    extra: k,
    hoverable: P,
    loading: x,
    size: E,
    tab_bar_extra_content: N,
    tab_list: j,
    tab_props: A,
    title: I,
    type: p,
    class_names: O,
    styles: q
  });
  return Y(t, V, (o) => i(0, l = o)), t.$$set = (o) => {
    "gradio" in o && i(6, u = o.gradio), "_internal" in o && i(7, d = o._internal), "actions" in o && i(8, b = o.actions), "active_tab_key" in o && i(9, h = o.active_tab_key), "bordered" in o && i(10, c = o.bordered), "cover" in o && i(11, m = o.cover), "default_active_tab_key" in o && i(12, y = o.default_active_tab_key), "extra" in o && i(13, k = o.extra), "hoverable" in o && i(14, P = o.hoverable), "loading" in o && i(15, x = o.loading), "size" in o && i(16, E = o.size), "tab_bar_extra_content" in o && i(17, N = o.tab_bar_extra_content), "tab_list" in o && i(18, j = o.tab_list), "tab_props" in o && i(19, A = o.tab_props), "title" in o && i(20, I = o.title), "type" in o && i(21, p = o.type), "class_names" in o && i(22, O = o.class_names), "styles" in o && i(23, q = o.styles), "as_item" in o && i(24, T = o.as_item), "props" in o && i(25, B = o.props), "elem_id" in o && i(26, L = o.elem_id), "elem_classes" in o && i(27, G = o.elem_classes), "elem_style" in o && i(28, R = o.elem_style), "visible" in o && i(29, U = o.visible), "$$scope" in o && i(32, _ = o.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty[0] & /*props*/
    33554432 && X.update((o) => ({
      ...o,
      ...B
    })), t.$$.dirty[0] & /*gradio, $updatedProps, _internal, as_item, visible, elem_id, elem_classes, elem_style, actions, active_tab_key, bordered, cover, default_active_tab_key, extra, hoverable, loading, size, tab_bar_extra_content, tab_list, tab_props, title, type, class_names, styles*/
    2113929152 && le({
      gradio: u,
      props: s,
      _internal: d,
      as_item: T,
      visible: U,
      elem_id: L,
      elem_classes: G,
      elem_style: R,
      actions: b,
      active_tab_key: h,
      bordered: c,
      cover: m,
      default_active_tab_key: y,
      extra: k,
      hoverable: P,
      loading: x,
      size: E,
      tab_bar_extra_content: N,
      tab_list: j,
      tab_props: A,
      title: I,
      type: p,
      class_names: O,
      styles: q
    });
  }, [l, n, a, X, M, V, u, d, b, h, c, m, y, k, P, x, E, N, j, A, I, p, O, q, T, B, L, G, R, U, s, r, _];
}
class Me extends Ce {
  constructor(e) {
    super(), pe(this, e, Ye, Xe, qe, {
      gradio: 6,
      _internal: 7,
      actions: 8,
      active_tab_key: 9,
      bordered: 10,
      cover: 11,
      default_active_tab_key: 12,
      extra: 13,
      hoverable: 14,
      loading: 15,
      size: 16,
      tab_bar_extra_content: 17,
      tab_list: 18,
      tab_props: 19,
      title: 20,
      type: 21,
      class_names: 22,
      styles: 23,
      as_item: 24,
      props: 25,
      elem_id: 26,
      elem_classes: 27,
      elem_style: 28,
      visible: 29
    }, null, [-1, -1]);
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), f();
  }
  get _internal() {
    return this.$$.ctx[7];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), f();
  }
  get actions() {
    return this.$$.ctx[8];
  }
  set actions(e) {
    this.$$set({
      actions: e
    }), f();
  }
  get active_tab_key() {
    return this.$$.ctx[9];
  }
  set active_tab_key(e) {
    this.$$set({
      active_tab_key: e
    }), f();
  }
  get bordered() {
    return this.$$.ctx[10];
  }
  set bordered(e) {
    this.$$set({
      bordered: e
    }), f();
  }
  get cover() {
    return this.$$.ctx[11];
  }
  set cover(e) {
    this.$$set({
      cover: e
    }), f();
  }
  get default_active_tab_key() {
    return this.$$.ctx[12];
  }
  set default_active_tab_key(e) {
    this.$$set({
      default_active_tab_key: e
    }), f();
  }
  get extra() {
    return this.$$.ctx[13];
  }
  set extra(e) {
    this.$$set({
      extra: e
    }), f();
  }
  get hoverable() {
    return this.$$.ctx[14];
  }
  set hoverable(e) {
    this.$$set({
      hoverable: e
    }), f();
  }
  get loading() {
    return this.$$.ctx[15];
  }
  set loading(e) {
    this.$$set({
      loading: e
    }), f();
  }
  get size() {
    return this.$$.ctx[16];
  }
  set size(e) {
    this.$$set({
      size: e
    }), f();
  }
  get tab_bar_extra_content() {
    return this.$$.ctx[17];
  }
  set tab_bar_extra_content(e) {
    this.$$set({
      tab_bar_extra_content: e
    }), f();
  }
  get tab_list() {
    return this.$$.ctx[18];
  }
  set tab_list(e) {
    this.$$set({
      tab_list: e
    }), f();
  }
  get tab_props() {
    return this.$$.ctx[19];
  }
  set tab_props(e) {
    this.$$set({
      tab_props: e
    }), f();
  }
  get title() {
    return this.$$.ctx[20];
  }
  set title(e) {
    this.$$set({
      title: e
    }), f();
  }
  get type() {
    return this.$$.ctx[21];
  }
  set type(e) {
    this.$$set({
      type: e
    }), f();
  }
  get class_names() {
    return this.$$.ctx[22];
  }
  set class_names(e) {
    this.$$set({
      class_names: e
    }), f();
  }
  get styles() {
    return this.$$.ctx[23];
  }
  set styles(e) {
    this.$$set({
      styles: e
    }), f();
  }
  get as_item() {
    return this.$$.ctx[24];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), f();
  }
  get props() {
    return this.$$.ctx[25];
  }
  set props(e) {
    this.$$set({
      props: e
    }), f();
  }
  get elem_id() {
    return this.$$.ctx[26];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), f();
  }
  get elem_classes() {
    return this.$$.ctx[27];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), f();
  }
  get elem_style() {
    return this.$$.ctx[28];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), f();
  }
  get visible() {
    return this.$$.ctx[29];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), f();
  }
}
export {
  Me as I,
  w as a,
  De as d,
  Fe as g,
  v as w
};
