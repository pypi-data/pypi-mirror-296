async function I() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((n) => {
    window.ms_globals.initialize = () => {
      n();
    };
  })), await window.ms_globals.initializePromise;
}
async function q(n) {
  return await I(), n().then((e) => e.default);
}
function p() {
}
function v(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function N(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return p;
  }
  const o = n.subscribe(...e);
  return o.unsubscribe ? () => o.unsubscribe() : o;
}
function _(n) {
  let e;
  return N(n, (o) => e = o)(), e;
}
const m = [];
function d(n, e = p) {
  let o;
  const t = /* @__PURE__ */ new Set();
  function i(c) {
    if (v(n, c) && (n = c, o)) {
      const r = !m.length;
      for (const l of t)
        l[1](), m.push(l, n);
      if (r) {
        for (let l = 0; l < m.length; l += 2)
          m[l][0](m[l + 1]);
        m.length = 0;
      }
    }
  }
  function s(c) {
    i(c(n));
  }
  function u(c, r = p) {
    const l = [c, r];
    return t.add(l), t.size === 1 && (o = e(i, s) || p), c(n), () => {
      t.delete(l), t.size === 0 && o && (o(), o = null);
    };
  }
  return {
    set: i,
    update: s,
    subscribe: u
  };
}
const {
  getContext: k,
  setContext: C
} = window.__gradio__svelte__internal, R = "$$ms-gr-antd-context-key";
function j(n) {
  var c;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = E(), o = F({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((r) => {
    o.slotKey.set(r);
  }), A();
  const t = k(R), i = ((c = _(t)) == null ? void 0 : c.as_item) || n.as_item, s = t ? i ? _(t)[i] : _(t) : {}, u = d({
    ...n,
    ...s
  });
  return t ? (t.subscribe((r) => {
    const {
      as_item: l
    } = _(u);
    l && (r = r[l]), u.update((h) => ({
      ...h,
      ...r
    }));
  }), [u, (r) => {
    const l = r.as_item ? _(t)[r.as_item] : _(t);
    return u.set({
      ...r,
      ...l
    });
  }]) : [u, (r) => {
    u.set(r);
  }];
}
const $ = "$$ms-gr-antd-slot-key";
function A() {
  C($, d(void 0));
}
function E() {
  return k($);
}
const x = "$$ms-gr-antd-component-slot-context-key";
function F({
  slot: n,
  index: e,
  subIndex: o
}) {
  return C(x, {
    slotKey: d(n),
    slotIndex: d(e),
    subSlotIndex: d(o)
  });
}
function st() {
  return k(x);
}
const {
  SvelteComponent: B,
  check_outros: D,
  component_subscribe: G,
  create_component: H,
  create_slot: J,
  destroy_component: L,
  detach: S,
  empty: K,
  flush: w,
  get_all_dirty_from_scope: M,
  get_slot_changes: O,
  group_outros: Q,
  handle_promise: T,
  init: U,
  insert: z,
  mount_component: V,
  noop: a,
  safe_not_equal: W,
  transition_in: b,
  transition_out: g,
  update_await_block_branch: X,
  update_slot_base: Y
} = window.__gradio__svelte__internal;
function y(n) {
  let e, o, t = {
    ctx: n,
    current: null,
    token: null,
    hasCatch: !1,
    pending: nt,
    then: tt,
    catch: Z,
    value: 9,
    blocks: [, , ,]
  };
  return T(
    /*AwaitedFragment*/
    n[1],
    t
  ), {
    c() {
      e = K(), t.block.c();
    },
    m(i, s) {
      z(i, e, s), t.block.m(i, t.anchor = s), t.mount = () => e.parentNode, t.anchor = e, o = !0;
    },
    p(i, s) {
      n = i, X(t, n, s);
    },
    i(i) {
      o || (b(t.block), o = !0);
    },
    o(i) {
      for (let s = 0; s < 3; s += 1) {
        const u = t.blocks[s];
        g(u);
      }
      o = !1;
    },
    d(i) {
      i && S(e), t.block.d(i), t.token = null, t = null;
    }
  };
}
function Z(n) {
  return {
    c: a,
    m: a,
    p: a,
    i: a,
    o: a,
    d: a
  };
}
function tt(n) {
  let e, o;
  return e = new /*Fragment*/
  n[9]({
    props: {
      slots: {},
      $$slots: {
        default: [et]
      },
      $$scope: {
        ctx: n
      }
    }
  }), {
    c() {
      H(e.$$.fragment);
    },
    m(t, i) {
      V(e, t, i), o = !0;
    },
    p(t, i) {
      const s = {};
      i & /*$$scope*/
      128 && (s.$$scope = {
        dirty: i,
        ctx: t
      }), e.$set(s);
    },
    i(t) {
      o || (b(e.$$.fragment, t), o = !0);
    },
    o(t) {
      g(e.$$.fragment, t), o = !1;
    },
    d(t) {
      L(e, t);
    }
  };
}
function et(n) {
  let e;
  const o = (
    /*#slots*/
    n[6].default
  ), t = J(
    o,
    n,
    /*$$scope*/
    n[7],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(i, s) {
      t && t.m(i, s), e = !0;
    },
    p(i, s) {
      t && t.p && (!e || s & /*$$scope*/
      128) && Y(
        t,
        o,
        i,
        /*$$scope*/
        i[7],
        e ? O(
          o,
          /*$$scope*/
          i[7],
          s,
          null
        ) : M(
          /*$$scope*/
          i[7]
        ),
        null
      );
    },
    i(i) {
      e || (b(t, i), e = !0);
    },
    o(i) {
      g(t, i), e = !1;
    },
    d(i) {
      t && t.d(i);
    }
  };
}
function nt(n) {
  return {
    c: a,
    m: a,
    p: a,
    i: a,
    o: a,
    d: a
  };
}
function it(n) {
  let e, o, t = (
    /*$mergedProps*/
    n[0].visible && y(n)
  );
  return {
    c() {
      t && t.c(), e = K();
    },
    m(i, s) {
      t && t.m(i, s), z(i, e, s), o = !0;
    },
    p(i, [s]) {
      /*$mergedProps*/
      i[0].visible ? t ? (t.p(i, s), s & /*$mergedProps*/
      1 && b(t, 1)) : (t = y(i), t.c(), b(t, 1), t.m(e.parentNode, e)) : t && (Q(), g(t, 1, 1, () => {
        t = null;
      }), D());
    },
    i(i) {
      o || (b(t), o = !0);
    },
    o(i) {
      g(t), o = !1;
    },
    d(i) {
      i && S(e), t && t.d(i);
    }
  };
}
function ot(n, e, o) {
  let t, {
    $$slots: i = {},
    $$scope: s
  } = e;
  const u = q(() => import("./fragment-B4AcdlHh.js"));
  let {
    _internal: c = {}
  } = e, {
    as_item: r = void 0
  } = e, {
    visible: l = !0
  } = e;
  const [h, P] = j({
    _internal: c,
    visible: l,
    as_item: r
  });
  return G(n, h, (f) => o(0, t = f)), n.$$set = (f) => {
    "_internal" in f && o(3, c = f._internal), "as_item" in f && o(4, r = f.as_item), "visible" in f && o(5, l = f.visible), "$$scope" in f && o(7, s = f.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*_internal, visible, as_item*/
    56 && P({
      _internal: c,
      visible: l,
      as_item: r
    });
  }, [t, u, h, c, r, l, i, s];
}
class rt extends B {
  constructor(e) {
    super(), U(this, e, ot, it, W, {
      _internal: 3,
      as_item: 4,
      visible: 5
    });
  }
  get _internal() {
    return this.$$.ctx[3];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), w();
  }
  get as_item() {
    return this.$$.ctx[4];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), w();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), w();
  }
}
export {
  rt as I,
  st as g,
  d as w
};
