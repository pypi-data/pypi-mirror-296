async function Q() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((s) => {
    window.ms_globals.initialize = () => {
      s();
    };
  })), await window.ms_globals.initializePromise;
}
async function T(s) {
  return await Q(), s().then((e) => e.default);
}
function W(s) {
  const {
    gradio: e,
    _internal: o,
    ...n
  } = s;
  return Object.keys(o).reduce((i, t) => {
    const l = t.match(/bind_(.+)_event/);
    if (l) {
      const c = l[1], r = c.split("_"), a = (...m) => {
        const g = m.map((_) => m && typeof _ == "object" && (_.nativeEvent || _ instanceof Event) ? {
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
        return e.dispatch(c.replace(/[A-Z]/g, (_) => "_" + _.toLowerCase()), {
          payload: g,
          component: n
        });
      };
      if (r.length > 1) {
        let m = {
          ...n.props[r[0]] || {}
        };
        i[r[0]] = m;
        for (let _ = 1; _ < r.length - 1; _++) {
          const y = {
            ...n.props[r[_]] || {}
          };
          m[r[_]] = y, m = y;
        }
        const g = r[r.length - 1];
        return m[`on${g.slice(0, 1).toUpperCase()}${g.slice(1)}`] = a, i;
      }
      const f = r[0];
      i[`on${f.slice(0, 1).toUpperCase()}${f.slice(1)}`] = a;
    }
    return i;
  }, {});
}
function j() {
}
function $(s, e) {
  return s != s ? e == e : s !== e || s && typeof s == "object" || typeof s == "function";
}
function ee(s, ...e) {
  if (s == null) {
    for (const n of e)
      n(void 0);
    return j;
  }
  const o = s.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function w(s) {
  let e;
  return ee(s, (o) => e = o)(), e;
}
const C = [];
function k(s, e = j) {
  let o;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if ($(s, c) && (s = c, o)) {
      const r = !C.length;
      for (const a of n)
        a[1](), C.push(a, s);
      if (r) {
        for (let a = 0; a < C.length; a += 2)
          C[a][0](C[a + 1]);
        C.length = 0;
      }
    }
  }
  function t(c) {
    i(c(s));
  }
  function l(c, r = j) {
    const a = [c, r];
    return n.add(a), n.size === 1 && (o = e(i, t) || j), c(s), () => {
      n.delete(a), n.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: t,
    subscribe: l
  };
}
const {
  getContext: z,
  setContext: I
} = window.__gradio__svelte__internal, te = "$$ms-gr-antd-slots-key";
function ne() {
  const s = k({});
  return I(te, s);
}
const se = "$$ms-gr-antd-context-key";
function oe(s) {
  var c;
  if (!Reflect.has(s, "as_item") || !Reflect.has(s, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = le(), o = re({
    slot: void 0,
    index: s._internal.index,
    subIndex: s._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), ie();
  const n = z(se), i = ((c = w(n)) == null ? void 0 : c.as_item) || s.as_item, t = n ? i ? w(n)[i] : w(n) : {}, l = k({
    ...s,
    ...t
  });
  return n ? (n.subscribe((r) => {
    const {
      as_item: a
    } = w(l);
    a && (r = r[a]), l.update((f) => ({
      ...f,
      ...r
    }));
  }), [l, (r) => {
    const a = r.as_item ? w(n)[r.as_item] : w(n);
    return l.set({
      ...r,
      ...a
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const X = "$$ms-gr-antd-slot-key";
function ie() {
  I(X, k(void 0));
}
function le() {
  return z(X);
}
const Y = "$$ms-gr-antd-component-slot-context-key";
function re({
  slot: s,
  index: e,
  subIndex: o
}) {
  return I(Y, {
    slotKey: k(s),
    slotIndex: k(e),
    subSlotIndex: k(o)
  });
}
function je() {
  return z(Y);
}
function ce(s) {
  return s && s.__esModule && Object.prototype.hasOwnProperty.call(s, "default") ? s.default : s;
}
var B = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(s) {
  (function() {
    var e = {}.hasOwnProperty;
    function o() {
      for (var t = "", l = 0; l < arguments.length; l++) {
        var c = arguments[l];
        c && (t = i(t, n(c)));
      }
      return t;
    }
    function n(t) {
      if (typeof t == "string" || typeof t == "number")
        return t;
      if (typeof t != "object")
        return "";
      if (Array.isArray(t))
        return o.apply(null, t);
      if (t.toString !== Object.prototype.toString && !t.toString.toString().includes("[native code]"))
        return t.toString();
      var l = "";
      for (var c in t)
        e.call(t, c) && t[c] && (l = i(l, c));
      return l;
    }
    function i(t, l) {
      return l ? t ? t + " " + l : t + l : t;
    }
    s.exports ? (o.default = o, s.exports = o) : window.classNames = o;
  })();
})(B);
var ue = B.exports;
const ae = /* @__PURE__ */ ce(ue), {
  SvelteComponent: _e,
  assign: D,
  check_outros: F,
  component_subscribe: N,
  create_component: L,
  create_slot: fe,
  destroy_component: M,
  detach: E,
  empty: O,
  flush: b,
  get_all_dirty_from_scope: me,
  get_slot_changes: de,
  get_spread_object: V,
  get_spread_update: Z,
  group_outros: G,
  handle_promise: be,
  init: pe,
  insert: q,
  mount_component: H,
  noop: d,
  safe_not_equal: ge,
  transition_in: p,
  transition_out: h,
  update_await_block_branch: he,
  update_slot_base: ye
} = window.__gradio__svelte__internal;
function U(s) {
  let e, o, n = {
    ctx: s,
    current: null,
    token: null,
    hasCatch: !1,
    pending: xe,
    then: we,
    catch: ke,
    value: 20,
    blocks: [, , ,]
  };
  return be(
    /*AwaitedBadge*/
    s[2],
    n
  ), {
    c() {
      e = O(), n.block.c();
    },
    m(i, t) {
      q(i, e, t), n.block.m(i, n.anchor = t), n.mount = () => e.parentNode, n.anchor = e, o = !0;
    },
    p(i, t) {
      s = i, he(n, s, t);
    },
    i(i) {
      o || (p(n.block), o = !0);
    },
    o(i) {
      for (let t = 0; t < 3; t += 1) {
        const l = n.blocks[t];
        h(l);
      }
      o = !1;
    },
    d(i) {
      i && E(e), n.block.d(i), n.token = null, n = null;
    }
  };
}
function ke(s) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function we(s) {
  let e, o, n, i;
  const t = [Ke, Ce], l = [];
  function c(r, a) {
    return (
      /*$mergedProps*/
      r[0]._internal.layout ? 0 : 1
    );
  }
  return e = c(s), o = l[e] = t[e](s), {
    c() {
      o.c(), n = O();
    },
    m(r, a) {
      l[e].m(r, a), q(r, n, a), i = !0;
    },
    p(r, a) {
      let f = e;
      e = c(r), e === f ? l[e].p(r, a) : (G(), h(l[f], 1, 1, () => {
        l[f] = null;
      }), F(), o = l[e], o ? o.p(r, a) : (o = l[e] = t[e](r), o.c()), p(o, 1), o.m(n.parentNode, n));
    },
    i(r) {
      i || (p(o), i = !0);
    },
    o(r) {
      h(o), i = !1;
    },
    d(r) {
      r && E(n), l[e].d(r);
    }
  };
}
function Ce(s) {
  let e, o;
  const n = [
    /*badge_props*/
    s[1]
  ];
  let i = {};
  for (let t = 0; t < n.length; t += 1)
    i = D(i, n[t]);
  return e = new /*Badge*/
  s[20]({
    props: i
  }), {
    c() {
      L(e.$$.fragment);
    },
    m(t, l) {
      H(e, t, l), o = !0;
    },
    p(t, l) {
      const c = l & /*badge_props*/
      2 ? Z(n, [V(
        /*badge_props*/
        t[1]
      )]) : {};
      e.$set(c);
    },
    i(t) {
      o || (p(e.$$.fragment, t), o = !0);
    },
    o(t) {
      h(e.$$.fragment, t), o = !1;
    },
    d(t) {
      M(e, t);
    }
  };
}
function Ke(s) {
  let e, o;
  const n = [
    /*badge_props*/
    s[1]
  ];
  let i = {
    $$slots: {
      default: [Se]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let t = 0; t < n.length; t += 1)
    i = D(i, n[t]);
  return e = new /*Badge*/
  s[20]({
    props: i
  }), {
    c() {
      L(e.$$.fragment);
    },
    m(t, l) {
      H(e, t, l), o = !0;
    },
    p(t, l) {
      const c = l & /*badge_props*/
      2 ? Z(n, [V(
        /*badge_props*/
        t[1]
      )]) : {};
      l & /*$$scope*/
      262144 && (c.$$scope = {
        dirty: l,
        ctx: t
      }), e.$set(c);
    },
    i(t) {
      o || (p(e.$$.fragment, t), o = !0);
    },
    o(t) {
      h(e.$$.fragment, t), o = !1;
    },
    d(t) {
      M(e, t);
    }
  };
}
function Se(s) {
  let e;
  const o = (
    /*#slots*/
    s[17].default
  ), n = fe(
    o,
    s,
    /*$$scope*/
    s[18],
    null
  );
  return {
    c() {
      n && n.c();
    },
    m(i, t) {
      n && n.m(i, t), e = !0;
    },
    p(i, t) {
      n && n.p && (!e || t & /*$$scope*/
      262144) && ye(
        n,
        o,
        i,
        /*$$scope*/
        i[18],
        e ? de(
          o,
          /*$$scope*/
          i[18],
          t,
          null
        ) : me(
          /*$$scope*/
          i[18]
        ),
        null
      );
    },
    i(i) {
      e || (p(n, i), e = !0);
    },
    o(i) {
      h(n, i), e = !1;
    },
    d(i) {
      n && n.d(i);
    }
  };
}
function xe(s) {
  return {
    c: d,
    m: d,
    p: d,
    i: d,
    o: d,
    d
  };
}
function ve(s) {
  let e, o, n = (
    /*$mergedProps*/
    s[0].visible && U(s)
  );
  return {
    c() {
      n && n.c(), e = O();
    },
    m(i, t) {
      n && n.m(i, t), q(i, e, t), o = !0;
    },
    p(i, [t]) {
      /*$mergedProps*/
      i[0].visible ? n ? (n.p(i, t), t & /*$mergedProps*/
      1 && p(n, 1)) : (n = U(i), n.c(), p(n, 1), n.m(e.parentNode, e)) : n && (G(), h(n, 1, 1, () => {
        n = null;
      }), F());
    },
    i(i) {
      o || (p(n), o = !0);
    },
    o(i) {
      h(n), o = !1;
    },
    d(i) {
      i && E(e), n && n.d(i);
    }
  };
}
function Pe(s, e, o) {
  let n, i, t, l, {
    $$slots: c = {},
    $$scope: r
  } = e;
  const a = T(() => import("./badge-C64jFX-w.js"));
  let {
    gradio: f
  } = e, {
    props: m = {}
  } = e;
  const g = k(m);
  N(s, g, (u) => o(16, l = u));
  let {
    _internal: _ = {}
  } = e, {
    count: y = 0
  } = e, {
    as_item: K
  } = e, {
    visible: S = !0
  } = e, {
    elem_id: x = ""
  } = e, {
    elem_classes: v = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [A, J] = oe({
    gradio: f,
    props: l,
    _internal: _,
    count: y,
    visible: S,
    elem_id: x,
    elem_classes: v,
    elem_style: P,
    as_item: K
  });
  N(s, A, (u) => o(0, i = u));
  const R = ne();
  return N(s, R, (u) => o(15, t = u)), s.$$set = (u) => {
    "gradio" in u && o(6, f = u.gradio), "props" in u && o(7, m = u.props), "_internal" in u && o(8, _ = u._internal), "count" in u && o(9, y = u.count), "as_item" in u && o(10, K = u.as_item), "visible" in u && o(11, S = u.visible), "elem_id" in u && o(12, x = u.elem_id), "elem_classes" in u && o(13, v = u.elem_classes), "elem_style" in u && o(14, P = u.elem_style), "$$scope" in u && o(18, r = u.$$scope);
  }, s.$$.update = () => {
    s.$$.dirty & /*props*/
    128 && g.update((u) => ({
      ...u,
      ...m
    })), s.$$.dirty & /*gradio, $updatedProps, _internal, count, visible, elem_id, elem_classes, elem_style, as_item*/
    98112 && J({
      gradio: f,
      props: l,
      _internal: _,
      count: y,
      visible: S,
      elem_id: x,
      elem_classes: v,
      elem_style: P,
      as_item: K
    }), s.$$.dirty & /*$mergedProps, $slots*/
    32769 && o(1, n = {
      style: i.elem_style,
      className: ae(i.elem_classes, "ms-gr-antd-badge"),
      id: i.elem_id,
      ...i.props,
      ...W(i),
      slots: t,
      count: i.props.count || i.count
    });
  }, [i, n, a, g, A, R, f, m, _, y, K, S, x, v, P, t, l, c, r];
}
class Ne extends _e {
  constructor(e) {
    super(), pe(this, e, Pe, ve, ge, {
      gradio: 6,
      props: 7,
      _internal: 8,
      count: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), b();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get count() {
    return this.$$.ctx[9];
  }
  set count(e) {
    this.$$set({
      count: e
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
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), b();
  }
}
export {
  Ne as I,
  je as g,
  k as w
};
