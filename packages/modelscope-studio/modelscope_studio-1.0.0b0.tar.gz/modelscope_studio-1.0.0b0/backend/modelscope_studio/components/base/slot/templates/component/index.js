function v() {
}
function H(t, e) {
  return t != t ? e == e : t !== e || t && typeof t == "object" || typeof t == "function";
}
function J(t, ...e) {
  if (t == null) {
    for (const n of e)
      n(void 0);
    return v;
  }
  const s = t.subscribe(...e);
  return s.unsubscribe ? () => s.unsubscribe() : s;
}
function d(t) {
  let e;
  return J(t, (s) => e = s)(), e;
}
const g = [];
function _(t, e = v) {
  let s;
  const n = /* @__PURE__ */ new Set();
  function i(c) {
    if (H(t, c) && (t = c, s)) {
      const a = !g.length;
      for (const u of n)
        u[1](), g.push(u, t);
      if (a) {
        for (let u = 0; u < g.length; u += 2)
          g[u][0](g[u + 1]);
        g.length = 0;
      }
    }
  }
  function o(c) {
    i(c(t));
  }
  function l(c, a = v) {
    const u = [c, a];
    return n.add(u), n.size === 1 && (s = e(i, o) || v), c(t), () => {
      n.delete(u), n.size === 0 && s && (s(), s = null);
    };
  }
  return {
    set: i,
    update: o,
    subscribe: l
  };
}
const {
  getContext: C,
  setContext: K
} = window.__gradio__svelte__internal, L = "$$ms-gr-antd-slots-key";
function O() {
  const t = C(L) || _({});
  return (e, s, n) => {
    t.update((i) => {
      const o = {
        ...i
      };
      return e && Reflect.deleteProperty(o, e), {
        ...o,
        [s]: n
      };
    });
  };
}
const Q = "$$ms-gr-antd-render-slot-context-key";
function T() {
  return C(Q);
}
const M = "$$ms-gr-antd-context-key";
function U() {
  const t = _();
  return K(M, t), (e) => {
    t.set(e);
  };
}
function W(t) {
  var c;
  if (!Reflect.has(t, "as_item") || !Reflect.has(t, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = Z(), s = tt({
    slot: void 0,
    index: t._internal.index,
    subIndex: t._internal.subIndex
  });
  e && e.subscribe((a) => {
    s.slotKey.set(a);
  }), X();
  const n = C(M), i = ((c = d(n)) == null ? void 0 : c.as_item) || t.as_item, o = n ? i ? d(n)[i] : d(n) : {}, l = _({
    ...t,
    ...o
  });
  return n ? (n.subscribe((a) => {
    const {
      as_item: u
    } = d(l);
    u && (a = a[u]), l.update((m) => ({
      ...m,
      ...a
    }));
  }), [l, (a) => {
    const u = a.as_item ? d(n)[a.as_item] : d(n);
    return l.set({
      ...a,
      ...u
    });
  }]) : [l, (a) => {
    l.set(a);
  }];
}
const I = "$$ms-gr-antd-slot-key";
function X() {
  K(I, _(void 0));
}
function Y(t) {
  return K(I, _(t));
}
function Z() {
  return C(I);
}
const $ = "$$ms-gr-antd-component-slot-context-key";
function tt({
  slot: t,
  index: e,
  subIndex: s
}) {
  return K($, {
    slotKey: _(t),
    slotIndex: _(e),
    subSlotIndex: _(s)
  });
}
function et(t) {
  try {
    return typeof t == "string" ? new Function(`return (...args) => (${t})(...args)`)() : void 0;
  } catch {
    return;
  }
}
const {
  SvelteComponent: nt,
  binding_callbacks: st,
  check_outros: it,
  component_subscribe: q,
  create_slot: ot,
  detach: j,
  element: rt,
  empty: lt,
  flush: y,
  get_all_dirty_from_scope: ut,
  get_slot_changes: ct,
  group_outros: at,
  init: _t,
  insert: E,
  safe_not_equal: ft,
  set_custom_element_data: mt,
  transition_in: S,
  transition_out: F,
  update_slot_base: bt
} = window.__gradio__svelte__internal;
function V(t) {
  let e, s;
  const n = (
    /*#slots*/
    t[17].default
  ), i = ot(
    n,
    t,
    /*$$scope*/
    t[16],
    null
  );
  return {
    c() {
      e = rt("svelte-slot"), i && i.c(), mt(e, "class", "svelte-1y8zqvi");
    },
    m(o, l) {
      E(o, e, l), i && i.m(e, null), t[18](e), s = !0;
    },
    p(o, l) {
      i && i.p && (!s || l & /*$$scope*/
      65536) && bt(
        i,
        n,
        o,
        /*$$scope*/
        o[16],
        s ? ct(
          n,
          /*$$scope*/
          o[16],
          l,
          null
        ) : ut(
          /*$$scope*/
          o[16]
        ),
        null
      );
    },
    i(o) {
      s || (S(i, o), s = !0);
    },
    o(o) {
      F(i, o), s = !1;
    },
    d(o) {
      o && j(e), i && i.d(o), t[18](null);
    }
  };
}
function dt(t) {
  let e, s, n = (
    /*$mergedProps*/
    t[1].visible && V(t)
  );
  return {
    c() {
      n && n.c(), e = lt();
    },
    m(i, o) {
      n && n.m(i, o), E(i, e, o), s = !0;
    },
    p(i, [o]) {
      /*$mergedProps*/
      i[1].visible ? n ? (n.p(i, o), o & /*$mergedProps*/
      2 && S(n, 1)) : (n = V(i), n.c(), S(n, 1), n.m(e.parentNode, e)) : n && (at(), F(n, 1, 1, () => {
        n = null;
      }), it());
    },
    i(i) {
      s || (S(n), s = !0);
    },
    o(i) {
      F(n), s = !1;
    },
    d(i) {
      i && j(e), n && n.d(i);
    }
  };
}
function gt(t, e, s) {
  let n, i, o, l, c, {
    $$slots: a = {},
    $$scope: u
  } = e, {
    params_mapping: m
  } = e, {
    value: b = ""
  } = e, {
    visible: h = !0
  } = e, {
    as_item: x
  } = e, {
    _internal: p = {}
  } = e, {
    skip_context_value: k = !0
  } = e;
  const z = T();
  q(t, z, (r) => s(15, o = r));
  const [R, N] = W({
    _internal: p,
    value: b,
    visible: h,
    as_item: x,
    params_mapping: m,
    skip_context_value: k
  });
  q(t, R, (r) => s(1, c = r));
  const w = _();
  q(t, w, (r) => s(0, l = r));
  const A = O();
  let P, f = b;
  const B = Y(f), D = U();
  function G(r) {
    st[r ? "unshift" : "push"](() => {
      l = r, w.set(l);
    });
  }
  return t.$$set = (r) => {
    "params_mapping" in r && s(5, m = r.params_mapping), "value" in r && s(6, b = r.value), "visible" in r && s(7, h = r.visible), "as_item" in r && s(8, x = r.as_item), "_internal" in r && s(9, p = r._internal), "skip_context_value" in r && s(10, k = r.skip_context_value), "$$scope" in r && s(16, u = r.$$scope);
  }, t.$$.update = () => {
    t.$$.dirty & /*_internal, value, visible, as_item, params_mapping, skip_context_value*/
    2016 && N({
      _internal: p,
      value: b,
      visible: h,
      as_item: x,
      params_mapping: m,
      skip_context_value: k
    }), t.$$.dirty & /*$mergedProps*/
    2 && s(14, n = c.params_mapping), t.$$.dirty & /*paramsMapping*/
    16384 && s(13, i = et(n)), t.$$.dirty & /*$slot, $mergedProps, value, prevValue, currentValue*/
    6211 && l && c.value && (s(12, f = c.skip_context_value ? b : c.value), A(P || "", f, l), s(11, P = f)), t.$$.dirty & /*currentValue*/
    4096 && B.set(f), t.$$.dirty & /*$slotParams, currentValue, paramsMappingFn*/
    45056 && o && o[f] && i && D(i(...o[f]));
  }, [l, c, z, R, w, m, b, h, x, p, k, P, f, i, n, o, u, a, G];
}
class yt extends nt {
  constructor(e) {
    super(), _t(this, e, gt, dt, ft, {
      params_mapping: 5,
      value: 6,
      visible: 7,
      as_item: 8,
      _internal: 9,
      skip_context_value: 10
    });
  }
  get params_mapping() {
    return this.$$.ctx[5];
  }
  set params_mapping(e) {
    this.$$set({
      params_mapping: e
    }), y();
  }
  get value() {
    return this.$$.ctx[6];
  }
  set value(e) {
    this.$$set({
      value: e
    }), y();
  }
  get visible() {
    return this.$$.ctx[7];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), y();
  }
  get as_item() {
    return this.$$.ctx[8];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), y();
  }
  get _internal() {
    return this.$$.ctx[9];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), y();
  }
  get skip_context_value() {
    return this.$$.ctx[10];
  }
  set skip_context_value(e) {
    this.$$set({
      skip_context_value: e
    }), y();
  }
}
export {
  yt as default
};
