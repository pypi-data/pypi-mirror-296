function v() {
}
function Q(i, t) {
  return i != i ? t == t : i !== t || i && typeof i == "object" || typeof i == "function";
}
function T(i, ...t) {
  if (i == null) {
    for (const e of t)
      e(void 0);
    return v;
  }
  const o = i.subscribe(...t);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function d(i) {
  let t;
  return T(i, (o) => t = o)(), t;
}
const b = [];
function g(i, t = v) {
  let o;
  const e = /* @__PURE__ */ new Set();
  function n(u) {
    if (Q(i, u) && (i = u, o)) {
      const r = !b.length;
      for (const c of e)
        c[1](), b.push(c, i);
      if (r) {
        for (let c = 0; c < b.length; c += 2)
          b[c][0](b[c + 1]);
        b.length = 0;
      }
    }
  }
  function s(u) {
    n(u(i));
  }
  function l(u, r = v) {
    const c = [u, r];
    return e.add(c), e.size === 1 && (o = t(n, s) || v), u(i), () => {
      e.delete(c), e.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: n,
    update: s,
    subscribe: l
  };
}
const {
  getContext: C,
  setContext: I
} = window.__gradio__svelte__internal, F = "$$ms-gr-antd-context-key";
function U() {
  const i = g();
  return I(F, i), (t) => {
    i.set(t);
  };
}
function R(i) {
  var u;
  if (!Reflect.has(i, "as_item") || !Reflect.has(i, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = W(), o = X({
    slot: void 0,
    index: i._internal.index,
    subIndex: i._internal.subIndex
  });
  t && t.subscribe((r) => {
    o.slotKey.set(r);
  }), V();
  const e = C(F), n = ((u = d(e)) == null ? void 0 : u.as_item) || i.as_item, s = e ? n ? d(e)[n] : d(e) : {}, l = g({
    ...i,
    ...s
  });
  return e ? (e.subscribe((r) => {
    const {
      as_item: c
    } = d(l);
    c && (r = r[c]), l.update((m) => ({
      ...m,
      ...r
    }));
  }), [l, (r) => {
    const c = r.as_item ? d(e)[r.as_item] : d(e);
    return l.set({
      ...r,
      ...c
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const j = "$$ms-gr-antd-slot-key";
function V() {
  I(j, g(void 0));
}
function W() {
  return C(j);
}
const A = "$$ms-gr-antd-component-slot-context-key";
function X({
  slot: i,
  index: t,
  subIndex: o
}) {
  return I(A, {
    slotKey: g(i),
    slotIndex: g(t),
    subSlotIndex: g(o)
  });
}
function Ye() {
  return C(A);
}
async function Y() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((i) => {
    window.ms_globals.initialize = () => {
      i();
    };
  })), await window.ms_globals.initializePromise;
}
async function Z(i) {
  return await Y(), i().then((t) => t.default);
}
const {
  SvelteComponent: ee,
  check_outros: te,
  component_subscribe: ne,
  create_component: ie,
  create_slot: oe,
  destroy_component: se,
  detach: B,
  empty: D,
  flush: x,
  get_all_dirty_from_scope: le,
  get_slot_changes: re,
  group_outros: ue,
  handle_promise: ce,
  init: _e,
  insert: G,
  mount_component: ae,
  noop: a,
  safe_not_equal: fe,
  transition_in: h,
  transition_out: p,
  update_await_block_branch: me,
  update_slot_base: de
} = window.__gradio__svelte__internal;
function P(i) {
  let t, o, e = {
    ctx: i,
    current: null,
    token: null,
    hasCatch: !1,
    pending: $e,
    then: ge,
    catch: be,
    value: 9,
    blocks: [, , ,]
  };
  return ce(
    /*AwaitedFragment*/
    i[1],
    e
  ), {
    c() {
      t = D(), e.block.c();
    },
    m(n, s) {
      G(n, t, s), e.block.m(n, e.anchor = s), e.mount = () => t.parentNode, e.anchor = t, o = !0;
    },
    p(n, s) {
      i = n, me(e, i, s);
    },
    i(n) {
      o || (h(e.block), o = !0);
    },
    o(n) {
      for (let s = 0; s < 3; s += 1) {
        const l = e.blocks[s];
        p(l);
      }
      o = !1;
    },
    d(n) {
      n && B(t), e.block.d(n), e.token = null, e = null;
    }
  };
}
function be(i) {
  return {
    c: a,
    m: a,
    p: a,
    i: a,
    o: a,
    d: a
  };
}
function ge(i) {
  let t, o;
  return t = new /*Fragment*/
  i[9]({
    props: {
      slots: {},
      $$slots: {
        default: [he]
      },
      $$scope: {
        ctx: i
      }
    }
  }), {
    c() {
      ie(t.$$.fragment);
    },
    m(e, n) {
      ae(t, e, n), o = !0;
    },
    p(e, n) {
      const s = {};
      n & /*$$scope*/
      128 && (s.$$scope = {
        dirty: n,
        ctx: e
      }), t.$set(s);
    },
    i(e) {
      o || (h(t.$$.fragment, e), o = !0);
    },
    o(e) {
      p(t.$$.fragment, e), o = !1;
    },
    d(e) {
      se(t, e);
    }
  };
}
function he(i) {
  let t;
  const o = (
    /*#slots*/
    i[6].default
  ), e = oe(
    o,
    i,
    /*$$scope*/
    i[7],
    null
  );
  return {
    c() {
      e && e.c();
    },
    m(n, s) {
      e && e.m(n, s), t = !0;
    },
    p(n, s) {
      e && e.p && (!t || s & /*$$scope*/
      128) && de(
        e,
        o,
        n,
        /*$$scope*/
        n[7],
        t ? re(
          o,
          /*$$scope*/
          n[7],
          s,
          null
        ) : le(
          /*$$scope*/
          n[7]
        ),
        null
      );
    },
    i(n) {
      t || (h(e, n), t = !0);
    },
    o(n) {
      p(e, n), t = !1;
    },
    d(n) {
      e && e.d(n);
    }
  };
}
function $e(i) {
  return {
    c: a,
    m: a,
    p: a,
    i: a,
    o: a,
    d: a
  };
}
function pe(i) {
  let t, o, e = (
    /*$mergedProps*/
    i[0].visible && P(i)
  );
  return {
    c() {
      e && e.c(), t = D();
    },
    m(n, s) {
      e && e.m(n, s), G(n, t, s), o = !0;
    },
    p(n, [s]) {
      /*$mergedProps*/
      n[0].visible ? e ? (e.p(n, s), s & /*$mergedProps*/
      1 && h(e, 1)) : (e = P(n), e.c(), h(e, 1), e.m(t.parentNode, t)) : e && (ue(), p(e, 1, 1, () => {
        e = null;
      }), te());
    },
    i(n) {
      o || (h(e), o = !0);
    },
    o(n) {
      p(e), o = !1;
    },
    d(n) {
      n && B(t), e && e.d(n);
    }
  };
}
function ke(i, t, o) {
  let e, {
    $$slots: n = {},
    $$scope: s
  } = t;
  const l = Z(() => import("./fragment-BNjhWNku.js"));
  let {
    _internal: u = {}
  } = t, {
    as_item: r = void 0
  } = t, {
    visible: c = !0
  } = t;
  const [m, w] = R({
    _internal: u,
    visible: c,
    as_item: r
  });
  return ne(i, m, (_) => o(0, e = _)), i.$$set = (_) => {
    "_internal" in _ && o(3, u = _._internal), "as_item" in _ && o(4, r = _.as_item), "visible" in _ && o(5, c = _.visible), "$$scope" in _ && o(7, s = _.$$scope);
  }, i.$$.update = () => {
    i.$$.dirty & /*_internal, visible, as_item*/
    56 && w({
      _internal: u,
      visible: c,
      as_item: r
    });
  }, [e, l, m, u, r, c, n, s];
}
let ve = class extends ee {
  constructor(t) {
    super(), _e(this, t, ke, pe, fe, {
      _internal: 3,
      as_item: 4,
      visible: 5
    });
  }
  get _internal() {
    return this.$$.ctx[3];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), x();
  }
  get as_item() {
    return this.$$.ctx[4];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), x();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), x();
  }
};
const {
  SvelteComponent: we,
  create_component: xe,
  create_slot: ye,
  destroy_component: Ce,
  flush: y,
  get_all_dirty_from_scope: Ie,
  get_slot_changes: Se,
  init: qe,
  mount_component: Pe,
  safe_not_equal: Ke,
  transition_in: H,
  transition_out: J,
  update_slot_base: ze
} = window.__gradio__svelte__internal;
function Ne(i) {
  let t;
  const o = (
    /*#slots*/
    i[3].default
  ), e = ye(
    o,
    i,
    /*$$scope*/
    i[4],
    null
  );
  return {
    c() {
      e && e.c();
    },
    m(n, s) {
      e && e.m(n, s), t = !0;
    },
    p(n, s) {
      e && e.p && (!t || s & /*$$scope*/
      16) && ze(
        e,
        o,
        n,
        /*$$scope*/
        n[4],
        t ? Se(
          o,
          /*$$scope*/
          n[4],
          s,
          null
        ) : Ie(
          /*$$scope*/
          n[4]
        ),
        null
      );
    },
    i(n) {
      t || (H(e, n), t = !0);
    },
    o(n) {
      J(e, n), t = !1;
    },
    d(n) {
      e && e.d(n);
    }
  };
}
function Ee(i) {
  let t, o;
  return t = new ve({
    props: {
      _internal: {
        index: (
          /*index*/
          i[0]
        ),
        subIndex: (
          /*subIndex*/
          i[1]
        )
      },
      $$slots: {
        default: [Ne]
      },
      $$scope: {
        ctx: i
      }
    }
  }), {
    c() {
      xe(t.$$.fragment);
    },
    m(e, n) {
      Pe(t, e, n), o = !0;
    },
    p(e, [n]) {
      const s = {};
      n & /*index, subIndex*/
      3 && (s._internal = {
        index: (
          /*index*/
          e[0]
        ),
        subIndex: (
          /*subIndex*/
          e[1]
        )
      }), n & /*$$scope*/
      16 && (s.$$scope = {
        dirty: n,
        ctx: e
      }), t.$set(s);
    },
    i(e) {
      o || (H(t.$$.fragment, e), o = !0);
    },
    o(e) {
      J(t.$$.fragment, e), o = !1;
    },
    d(e) {
      Ce(t, e);
    }
  };
}
function Fe(i, t, o) {
  let {
    $$slots: e = {},
    $$scope: n
  } = t, {
    index: s
  } = t, {
    subIndex: l
  } = t, {
    value: u
  } = t;
  const r = U();
  return r(u), i.$$set = (c) => {
    "index" in c && o(0, s = c.index), "subIndex" in c && o(1, l = c.subIndex), "value" in c && o(2, u = c.value), "$$scope" in c && o(4, n = c.$$scope);
  }, i.$$.update = () => {
    i.$$.dirty & /*value*/
    4 && r(u);
  }, [s, l, u, e, n];
}
class Re extends we {
  constructor(t) {
    super(), qe(this, t, Fe, Ee, Ke, {
      index: 0,
      subIndex: 1,
      value: 2
    });
  }
  get index() {
    return this.$$.ctx[0];
  }
  set index(t) {
    this.$$set({
      index: t
    }), y();
  }
  get subIndex() {
    return this.$$.ctx[1];
  }
  set subIndex(t) {
    this.$$set({
      subIndex: t
    }), y();
  }
  get value() {
    return this.$$.ctx[2];
  }
  set value(t) {
    this.$$set({
      value: t
    }), y();
  }
}
const {
  SvelteComponent: je,
  check_outros: L,
  component_subscribe: Ae,
  create_component: Be,
  create_slot: De,
  destroy_component: Ge,
  destroy_each: He,
  detach: S,
  empty: M,
  ensure_array_like: K,
  flush: k,
  get_all_dirty_from_scope: Je,
  get_slot_changes: Le,
  group_outros: O,
  init: Me,
  insert: q,
  mount_component: Oe,
  safe_not_equal: Qe,
  space: Te,
  transition_in: f,
  transition_out: $,
  update_slot_base: Ue
} = window.__gradio__svelte__internal;
function z(i, t, o) {
  const e = i.slice();
  return e[9] = t[o], e[11] = o, e;
}
function N(i) {
  let t, o, e = K(
    /*$mergedProps*/
    i[0].value
  ), n = [];
  for (let l = 0; l < e.length; l += 1)
    n[l] = E(z(i, e, l));
  const s = (l) => $(n[l], 1, 1, () => {
    n[l] = null;
  });
  return {
    c() {
      for (let l = 0; l < n.length; l += 1)
        n[l].c();
      t = M();
    },
    m(l, u) {
      for (let r = 0; r < n.length; r += 1)
        n[r] && n[r].m(l, u);
      q(l, t, u), o = !0;
    },
    p(l, u) {
      if (u & /*$mergedProps, $$scope*/
      129) {
        e = K(
          /*$mergedProps*/
          l[0].value
        );
        let r;
        for (r = 0; r < e.length; r += 1) {
          const c = z(l, e, r);
          n[r] ? (n[r].p(c, u), f(n[r], 1)) : (n[r] = E(c), n[r].c(), f(n[r], 1), n[r].m(t.parentNode, t));
        }
        for (O(), r = e.length; r < n.length; r += 1)
          s(r);
        L();
      }
    },
    i(l) {
      if (!o) {
        for (let u = 0; u < e.length; u += 1)
          f(n[u]);
        o = !0;
      }
    },
    o(l) {
      n = n.filter(Boolean);
      for (let u = 0; u < n.length; u += 1)
        $(n[u]);
      o = !1;
    },
    d(l) {
      l && S(t), He(n, l);
    }
  };
}
function Ve(i) {
  let t, o;
  const e = (
    /*#slots*/
    i[6].default
  ), n = De(
    e,
    i,
    /*$$scope*/
    i[7],
    null
  );
  return {
    c() {
      n && n.c(), t = Te();
    },
    m(s, l) {
      n && n.m(s, l), q(s, t, l), o = !0;
    },
    p(s, l) {
      n && n.p && (!o || l & /*$$scope*/
      128) && Ue(
        n,
        e,
        s,
        /*$$scope*/
        s[7],
        o ? Le(
          e,
          /*$$scope*/
          s[7],
          l,
          null
        ) : Je(
          /*$$scope*/
          s[7]
        ),
        null
      );
    },
    i(s) {
      o || (f(n, s), o = !0);
    },
    o(s) {
      $(n, s), o = !1;
    },
    d(s) {
      s && S(t), n && n.d(s);
    }
  };
}
function E(i) {
  let t, o;
  return t = new Re({
    props: {
      value: (
        /*item*/
        i[9]
      ),
      index: (
        /*$mergedProps*/
        i[0]._internal.index || 0
      ),
      subIndex: (
        /*i*/
        i[11]
      ),
      $$slots: {
        default: [Ve]
      },
      $$scope: {
        ctx: i
      }
    }
  }), {
    c() {
      Be(t.$$.fragment);
    },
    m(e, n) {
      Oe(t, e, n), o = !0;
    },
    p(e, n) {
      const s = {};
      n & /*$mergedProps*/
      1 && (s.value = /*item*/
      e[9]), n & /*$mergedProps*/
      1 && (s.index = /*$mergedProps*/
      e[0]._internal.index || 0), n & /*$$scope*/
      128 && (s.$$scope = {
        dirty: n,
        ctx: e
      }), t.$set(s);
    },
    i(e) {
      o || (f(t.$$.fragment, e), o = !0);
    },
    o(e) {
      $(t.$$.fragment, e), o = !1;
    },
    d(e) {
      Ge(t, e);
    }
  };
}
function We(i) {
  let t, o, e = (
    /*$mergedProps*/
    i[0].visible && N(i)
  );
  return {
    c() {
      e && e.c(), t = M();
    },
    m(n, s) {
      e && e.m(n, s), q(n, t, s), o = !0;
    },
    p(n, [s]) {
      /*$mergedProps*/
      n[0].visible ? e ? (e.p(n, s), s & /*$mergedProps*/
      1 && f(e, 1)) : (e = N(n), e.c(), f(e, 1), e.m(t.parentNode, t)) : e && (O(), $(e, 1, 1, () => {
        e = null;
      }), L());
    },
    i(n) {
      o || (f(e), o = !0);
    },
    o(n) {
      $(e), o = !1;
    },
    d(n) {
      n && S(t), e && e.d(n);
    }
  };
}
function Xe(i, t, o) {
  let e, {
    $$slots: n = {},
    $$scope: s
  } = t, {
    value: l = []
  } = t, {
    as_item: u
  } = t, {
    visible: r = !0
  } = t, {
    _internal: c = {}
  } = t;
  const [m, w] = R({
    _internal: c,
    value: l,
    as_item: u,
    visible: r
  });
  return Ae(i, m, (_) => o(0, e = _)), i.$$set = (_) => {
    "value" in _ && o(2, l = _.value), "as_item" in _ && o(3, u = _.as_item), "visible" in _ && o(4, r = _.visible), "_internal" in _ && o(5, c = _._internal), "$$scope" in _ && o(7, s = _.$$scope);
  }, i.$$.update = () => {
    i.$$.dirty & /*_internal, value, as_item, visible*/
    60 && w({
      _internal: c,
      value: l,
      as_item: u,
      visible: r
    });
  }, [e, m, l, u, r, c, n, s];
}
class et extends je {
  constructor(t) {
    super(), Me(this, t, Xe, We, Qe, {
      value: 2,
      as_item: 3,
      visible: 4,
      _internal: 5
    });
  }
  get value() {
    return this.$$.ctx[2];
  }
  set value(t) {
    this.$$set({
      value: t
    }), k();
  }
  get as_item() {
    return this.$$.ctx[3];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), k();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), k();
  }
  get _internal() {
    return this.$$.ctx[5];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), k();
  }
}
export {
  et as I,
  Ye as g,
  g as w
};
