function d() {
}
function I(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function p(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return d;
  }
  const s = n.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function f(n) {
  let e;
  return p(n, (s) => e = s)(), e;
}
const a = [];
function b(n, e = d) {
  let s;
  const t = /* @__PURE__ */ new Set();
  function i(u) {
    if (I(n, u) && (n = u, s)) {
      const o = !a.length;
      for (const l of t)
        l[1](), a.push(l, n);
      if (o) {
        for (let l = 0; l < a.length; l += 2)
          a[l][0](a[l + 1]);
        a.length = 0;
      }
    }
  }
  function r(u) {
    i(u(n));
  }
  function c(u, o = d) {
    const l = [u, o];
    return t.add(l), t.size === 1 && (s = e(i, r) || d), u(n), () => {
      t.delete(l), t.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: r,
    subscribe: c
  };
}
const {
  getContext: K,
  setContext: y
} = window.__gradio__svelte__internal, k = "$$ms-gr-antd-context-key";
function P() {
  const n = b();
  return y(k, n), (e) => {
    n.set(e);
  };
}
function z(n) {
  var u;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = j(), s = F({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((o) => {
    s.slotKey.set(o);
  }), R();
  const t = K(k), i = ((u = f(t)) == null ? void 0 : u.as_item) || n.as_item, r = t ? i ? f(t)[i] : f(t) : {}, c = b({
    ...n,
    ...r
  });
  return t ? (t.subscribe((o) => {
    const {
      as_item: l
    } = f(c);
    l && (o = o[l]), c.update((g) => ({
      ...g,
      ...o
    }));
  }), [c, (o) => {
    const l = o.as_item ? f(t)[o.as_item] : f(t);
    return c.set({
      ...o,
      ...l
    });
  }]) : [c, (o) => {
    c.set(o);
  }];
}
const v = "$$ms-gr-antd-slot-key";
function R() {
  y(v, b(void 0));
}
function j() {
  return K(v);
}
const E = "$$ms-gr-antd-component-slot-context-key";
function F({
  slot: n,
  index: e,
  subIndex: s
}) {
  return y(E, {
    slotKey: b(n),
    slotIndex: b(e),
    subSlotIndex: b(s)
  });
}
const {
  SvelteComponent: N,
  check_outros: A,
  component_subscribe: B,
  create_slot: D,
  detach: G,
  empty: H,
  flush: h,
  get_all_dirty_from_scope: J,
  get_slot_changes: L,
  group_outros: M,
  init: O,
  insert: Q,
  safe_not_equal: T,
  transition_in: m,
  transition_out: x,
  update_slot_base: U
} = window.__gradio__svelte__internal;
function S(n) {
  let e;
  const s = (
    /*#slots*/
    n[6].default
  ), t = D(
    s,
    n,
    /*$$scope*/
    n[5],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(i, r) {
      t && t.m(i, r), e = !0;
    },
    p(i, r) {
      t && t.p && (!e || r & /*$$scope*/
      32) && U(
        t,
        s,
        i,
        /*$$scope*/
        i[5],
        e ? L(
          s,
          /*$$scope*/
          i[5],
          r,
          null
        ) : J(
          /*$$scope*/
          i[5]
        ),
        null
      );
    },
    i(i) {
      e || (m(t, i), e = !0);
    },
    o(i) {
      x(t, i), e = !1;
    },
    d(i) {
      t && t.d(i);
    }
  };
}
function V(n) {
  let e, s, t = (
    /*$mergedProps*/
    n[0].visible && S(n)
  );
  return {
    c() {
      t && t.c(), e = H();
    },
    m(i, r) {
      t && t.m(i, r), Q(i, e, r), s = !0;
    },
    p(i, [r]) {
      /*$mergedProps*/
      i[0].visible ? t ? (t.p(i, r), r & /*$mergedProps*/
      1 && m(t, 1)) : (t = S(i), t.c(), m(t, 1), t.m(e.parentNode, e)) : t && (M(), x(t, 1, 1, () => {
        t = null;
      }), A());
    },
    i(i) {
      s || (m(t), s = !0);
    },
    o(i) {
      x(t), s = !1;
    },
    d(i) {
      i && G(e), t && t.d(i);
    }
  };
}
function W(n, e, s) {
  let t, {
    $$slots: i = {},
    $$scope: r
  } = e, {
    as_item: c
  } = e, {
    visible: u = !0
  } = e, {
    _internal: o = {}
  } = e;
  const [l, g] = z({
    _internal: o,
    as_item: c,
    visible: u
  });
  B(n, l, (_) => s(0, t = _));
  const C = P();
  return n.$$set = (_) => {
    "as_item" in _ && s(2, c = _.as_item), "visible" in _ && s(3, u = _.visible), "_internal" in _ && s(4, o = _._internal), "$$scope" in _ && s(5, r = _.$$scope);
  }, n.$$.update = () => {
    if (n.$$.dirty & /*_internal, as_item, visible*/
    28 && g({
      _internal: o,
      as_item: c,
      visible: u
    }), n.$$.dirty & /*$mergedProps*/
    1) {
      const {
        _internal: _,
        as_item: w,
        visible: X,
        ...q
      } = t;
      C(w ? q : void 0);
    }
  }, [t, l, c, u, o, r, i];
}
class Y extends N {
  constructor(e) {
    super(), O(this, e, W, V, T, {
      as_item: 2,
      visible: 3,
      _internal: 4
    });
  }
  get as_item() {
    return this.$$.ctx[2];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), h();
  }
  get visible() {
    return this.$$.ctx[3];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), h();
  }
  get _internal() {
    return this.$$.ctx[4];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), h();
  }
}
export {
  Y as default
};
