function x() {
}
function F(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function O(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return x;
  }
  const s = n.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function m(n) {
  let e;
  return O(n, (s) => e = s)(), e;
}
const d = [];
function f(n, e = x) {
  let s;
  const t = /* @__PURE__ */ new Set();
  function i(u) {
    if (F(n, u) && (n = u, s)) {
      const c = !d.length;
      for (const r of t)
        r[1](), d.push(r, n);
      if (c) {
        for (let r = 0; r < d.length; r += 2)
          d[r][0](d[r + 1]);
        d.length = 0;
      }
    }
  }
  function l(u) {
    i(u(n));
  }
  function _(u, c = x) {
    const r = [u, c];
    return t.add(r), t.size === 1 && (s = e(i, l) || x), u(n), () => {
      t.delete(r), t.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: l,
    subscribe: _
  };
}
const {
  getContext: P,
  setContext: k
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-context-key";
function R(n) {
  var u;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = v(), s = U({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((c) => {
    s.slotKey.set(c);
  }), j();
  const t = P(J), i = ((u = m(t)) == null ? void 0 : u.as_item) || n.as_item, l = t ? i ? m(t)[i] : m(t) : {}, _ = f({
    ...n,
    ...l
  });
  return t ? (t.subscribe((c) => {
    const {
      as_item: r
    } = m(_);
    r && (c = c[r]), _.update((a) => ({
      ...a,
      ...c
    }));
  }), [_, (c) => {
    const r = c.as_item ? m(t)[c.as_item] : m(t);
    return _.set({
      ...c,
      ...r
    });
  }]) : [_, (c) => {
    _.set(c);
  }];
}
const z = "$$ms-gr-antd-slot-key";
function j() {
  k(z, f(void 0));
}
function v() {
  return P(z);
}
const E = "$$ms-gr-antd-component-slot-context-key";
function U({
  slot: n,
  index: e,
  subIndex: s
}) {
  return k(E, {
    slotKey: f(n),
    slotIndex: f(e),
    subSlotIndex: f(s)
  });
}
async function A() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((n) => {
    window.ms_globals.initialize = () => {
      n();
    };
  })), await window.ms_globals.initializePromise;
}
const {
  getContext: st,
  setContext: B
} = window.__gradio__svelte__internal, D = "$$ms-gr-antd-iconfont-context-key";
let w;
async function G() {
  return w || (await A(), w = await import("./create-iconfont-DTWKM8U_.js").then((n) => n.createFromIconfontCN), w);
}
function H() {
  const n = f(), e = f();
  return n.subscribe(async (s) => {
    const t = await G();
    e.set(t(s));
  }), B(D, e), n;
}
const {
  SvelteComponent: L,
  check_outros: M,
  component_subscribe: S,
  create_slot: Q,
  detach: T,
  empty: V,
  flush: b,
  get_all_dirty_from_scope: W,
  get_slot_changes: X,
  group_outros: Y,
  init: Z,
  insert: $,
  safe_not_equal: tt,
  transition_in: y,
  transition_out: h,
  update_slot_base: et
} = window.__gradio__svelte__internal;
function K(n) {
  let e;
  const s = (
    /*#slots*/
    n[10].default
  ), t = Q(
    s,
    n,
    /*$$scope*/
    n[9],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(i, l) {
      t && t.m(i, l), e = !0;
    },
    p(i, l) {
      t && t.p && (!e || l & /*$$scope*/
      512) && et(
        t,
        s,
        i,
        /*$$scope*/
        i[9],
        e ? X(
          s,
          /*$$scope*/
          i[9],
          l,
          null
        ) : W(
          /*$$scope*/
          i[9]
        ),
        null
      );
    },
    i(i) {
      e || (y(t, i), e = !0);
    },
    o(i) {
      h(t, i), e = !1;
    },
    d(i) {
      t && t.d(i);
    }
  };
}
function nt(n) {
  let e, s, t = (
    /*$mergedProps*/
    n[0].visible && K(n)
  );
  return {
    c() {
      t && t.c(), e = V();
    },
    m(i, l) {
      t && t.m(i, l), $(i, e, l), s = !0;
    },
    p(i, [l]) {
      /*$mergedProps*/
      i[0].visible ? t ? (t.p(i, l), l & /*$mergedProps*/
      1 && y(t, 1)) : (t = K(i), t.c(), y(t, 1), t.m(e.parentNode, e)) : t && (Y(), h(t, 1, 1, () => {
        t = null;
      }), M());
    },
    i(i) {
      s || (y(t), s = !0);
    },
    o(i) {
      h(t), s = !1;
    },
    d(i) {
      i && T(e), t && t.d(i);
    }
  };
}
function it(n, e, s) {
  let t, i, {
    $$slots: l = {},
    $$scope: _
  } = e, {
    props: u = {}
  } = e;
  const c = f(u);
  S(n, c, (o) => s(8, i = o));
  let {
    _internal: r = {}
  } = e, {
    script_url: a = ""
  } = e, {
    as_item: g
  } = e, {
    visible: p = !0
  } = e;
  const [C, q] = R({
    props: i,
    _internal: r,
    script_url: a,
    visible: p,
    as_item: g
  });
  S(n, C, (o) => s(0, t = o));
  const N = H();
  return n.$$set = (o) => {
    "props" in o && s(3, u = o.props), "_internal" in o && s(4, r = o._internal), "script_url" in o && s(5, a = o.script_url), "as_item" in o && s(6, g = o.as_item), "visible" in o && s(7, p = o.visible), "$$scope" in o && s(9, _ = o.$$scope);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*props*/
    8 && c.update((o) => ({
      ...o,
      ...u
    })), n.$$.dirty & /*$updatedProps, _internal, script_url, visible, as_item*/
    496 && q({
      props: i,
      _internal: r,
      script_url: a,
      visible: p,
      as_item: g
    }), n.$$.dirty & /*$mergedProps*/
    1) {
      const o = {
        scriptUrl: t.script_url,
        ...t.props
      };
      N.update((I) => JSON.stringify(I) !== JSON.stringify(o) ? o : I);
    }
  }, [t, c, C, u, r, a, g, p, i, _, l];
}
class ot extends L {
  constructor(e) {
    super(), Z(this, e, it, nt, tt, {
      props: 3,
      _internal: 4,
      script_url: 5,
      as_item: 6,
      visible: 7
    });
  }
  get props() {
    return this.$$.ctx[3];
  }
  set props(e) {
    this.$$set({
      props: e
    }), b();
  }
  get _internal() {
    return this.$$.ctx[4];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), b();
  }
  get script_url() {
    return this.$$.ctx[5];
  }
  set script_url(e) {
    this.$$set({
      script_url: e
    }), b();
  }
  get as_item() {
    return this.$$.ctx[6];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), b();
  }
  get visible() {
    return this.$$.ctx[7];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), b();
  }
}
export {
  ot as default
};
