async function K() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((s) => {
    window.ms_globals.initialize = () => {
      s();
    };
  })), await window.ms_globals.initializePromise;
}
async function w(s) {
  return await K(), s().then((e) => e.default);
}
function V(s) {
  const {
    gradio: e,
    _internal: o,
    ...t
  } = s;
  return Object.keys(o).reduce((l, r) => {
    const u = r.match(/bind_(.+)_event/);
    if (u) {
      const i = u[1], n = i.split("_"), f = (...m) => {
        const h = m.map((a) => m && typeof a == "object" && (a.nativeEvent || a instanceof Event) ? {
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
        return e.dispatch(i.replace(/[A-Z]/g, (a) => "_" + a.toLowerCase()), {
          payload: h,
          component: t
        });
      };
      if (n.length > 1) {
        let m = {
          ...t.props[n[0]] || {}
        };
        l[n[0]] = m;
        for (let a = 1; a < n.length - 1; a++) {
          const g = {
            ...t.props[n[a]] || {}
          };
          m[n[a]] = g, m = g;
        }
        const h = n[n.length - 1];
        return m[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = f, l;
      }
      const b = n[0];
      l[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f;
    }
    return l;
  }, {});
}
const {
  SvelteComponent: C,
  add_flush_callback: z,
  assign: v,
  bind: P,
  binding_callbacks: j,
  create_component: E,
  create_slot: I,
  destroy_component: N,
  detach: S,
  empty: A,
  exclude_internal_props: y,
  flush: d,
  get_all_dirty_from_scope: U,
  get_slot_changes: X,
  get_spread_object: Y,
  get_spread_update: q,
  handle_promise: L,
  init: O,
  insert: R,
  mount_component: Z,
  noop: _,
  safe_not_equal: B,
  transition_in: p,
  transition_out: k,
  update_await_block_branch: D,
  update_slot_base: F
} = window.__gradio__svelte__internal;
function G(s) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function H(s) {
  let e, o, t;
  const l = [
    /*$$props*/
    s[9],
    {
      gradio: (
        /*gradio*/
        s[1]
      )
    },
    {
      props: (
        /*props*/
        s[2]
      )
    },
    {
      as_item: (
        /*as_item*/
        s[3]
      )
    },
    {
      visible: (
        /*visible*/
        s[4]
      )
    },
    {
      elem_id: (
        /*elem_id*/
        s[5]
      )
    },
    {
      elem_classes: (
        /*elem_classes*/
        s[6]
      )
    },
    {
      elem_style: (
        /*elem_style*/
        s[7]
      )
    }
  ];
  function r(i) {
    s[11](i);
  }
  let u = {
    $$slots: {
      default: [J]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let i = 0; i < l.length; i += 1)
    u = v(u, l[i]);
  return (
    /*value*/
    s[0] !== void 0 && (u.value = /*value*/
    s[0]), e = new /*RowSelection*/
    s[13]({
      props: u
    }), j.push(() => P(e, "value", r)), {
      c() {
        E(e.$$.fragment);
      },
      m(i, n) {
        Z(e, i, n), t = !0;
      },
      p(i, n) {
        const f = n & /*$$props, gradio, props, as_item, visible, elem_id, elem_classes, elem_style*/
        766 ? q(l, [n & /*$$props*/
        512 && Y(
          /*$$props*/
          i[9]
        ), n & /*gradio*/
        2 && {
          gradio: (
            /*gradio*/
            i[1]
          )
        }, n & /*props*/
        4 && {
          props: (
            /*props*/
            i[2]
          )
        }, n & /*as_item*/
        8 && {
          as_item: (
            /*as_item*/
            i[3]
          )
        }, n & /*visible*/
        16 && {
          visible: (
            /*visible*/
            i[4]
          )
        }, n & /*elem_id*/
        32 && {
          elem_id: (
            /*elem_id*/
            i[5]
          )
        }, n & /*elem_classes*/
        64 && {
          elem_classes: (
            /*elem_classes*/
            i[6]
          )
        }, n & /*elem_style*/
        128 && {
          elem_style: (
            /*elem_style*/
            i[7]
          )
        }]) : {};
        n & /*$$scope*/
        4096 && (f.$$scope = {
          dirty: n,
          ctx: i
        }), !o && n & /*value*/
        1 && (o = !0, f.value = /*value*/
        i[0], z(() => o = !1)), e.$set(f);
      },
      i(i) {
        t || (p(e.$$.fragment, i), t = !0);
      },
      o(i) {
        k(e.$$.fragment, i), t = !1;
      },
      d(i) {
        N(e, i);
      }
    }
  );
}
function J(s) {
  let e;
  const o = (
    /*#slots*/
    s[10].default
  ), t = I(
    o,
    s,
    /*$$scope*/
    s[12],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(l, r) {
      t && t.m(l, r), e = !0;
    },
    p(l, r) {
      t && t.p && (!e || r & /*$$scope*/
      4096) && F(
        t,
        o,
        l,
        /*$$scope*/
        l[12],
        e ? X(
          o,
          /*$$scope*/
          l[12],
          r,
          null
        ) : U(
          /*$$scope*/
          l[12]
        ),
        null
      );
    },
    i(l) {
      e || (p(t, l), e = !0);
    },
    o(l) {
      k(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function M(s) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function Q(s) {
  let e, o, t = {
    ctx: s,
    current: null,
    token: null,
    hasCatch: !1,
    pending: M,
    then: H,
    catch: G,
    value: 13,
    blocks: [, , ,]
  };
  return L(
    /*AwaitedRowSelection*/
    s[8],
    t
  ), {
    c() {
      e = A(), t.block.c();
    },
    m(l, r) {
      R(l, e, r), t.block.m(l, t.anchor = r), t.mount = () => e.parentNode, t.anchor = e, o = !0;
    },
    p(l, [r]) {
      s = l, D(t, s, r);
    },
    i(l) {
      o || (p(t.block), o = !0);
    },
    o(l) {
      for (let r = 0; r < 3; r += 1) {
        const u = t.blocks[r];
        k(u);
      }
      o = !1;
    },
    d(l) {
      l && S(e), t.block.d(l), t.token = null, t = null;
    }
  };
}
function T(s, e, o) {
  let {
    $$slots: t = {},
    $$scope: l
  } = e;
  const r = w(() => import("./RowSelection-C5grFcLu.js"));
  let {
    gradio: u
  } = e, {
    props: i = {}
  } = e, {
    value: n
  } = e, {
    as_item: f
  } = e, {
    visible: b = !0
  } = e, {
    elem_id: m = ""
  } = e, {
    elem_classes: h = []
  } = e, {
    elem_style: a = {}
  } = e;
  function g(c) {
    n = c, o(0, n);
  }
  return s.$$set = (c) => {
    o(9, e = v(v({}, e), y(c))), "gradio" in c && o(1, u = c.gradio), "props" in c && o(2, i = c.props), "value" in c && o(0, n = c.value), "as_item" in c && o(3, f = c.as_item), "visible" in c && o(4, b = c.visible), "elem_id" in c && o(5, m = c.elem_id), "elem_classes" in c && o(6, h = c.elem_classes), "elem_style" in c && o(7, a = c.elem_style), "$$scope" in c && o(12, l = c.$$scope);
  }, e = y(e), [n, u, i, f, b, m, h, a, r, e, t, g, l];
}
class W extends C {
  constructor(e) {
    super(), O(this, e, T, Q, B, {
      gradio: 1,
      props: 2,
      value: 0,
      as_item: 3,
      visible: 4,
      elem_id: 5,
      elem_classes: 6,
      elem_style: 7
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), d();
  }
  get props() {
    return this.$$.ctx[2];
  }
  set props(e) {
    this.$$set({
      props: e
    }), d();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({
      value: e
    }), d();
  }
  get as_item() {
    return this.$$.ctx[3];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), d();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), d();
  }
  get elem_id() {
    return this.$$.ctx[5];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), d();
  }
  get elem_classes() {
    return this.$$.ctx[6];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), d();
  }
  get elem_style() {
    return this.$$.ctx[7];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), d();
  }
}
export {
  W as I,
  V as b
};
