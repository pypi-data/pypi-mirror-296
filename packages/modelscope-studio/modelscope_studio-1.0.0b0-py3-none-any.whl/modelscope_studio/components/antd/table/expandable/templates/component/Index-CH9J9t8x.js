async function K() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((s) => {
    window.ms_globals.initialize = () => {
      s();
    };
  })), await window.ms_globals.initializePromise;
}
async function C(s) {
  return await K(), s().then((e) => e.default);
}
function V(s) {
  const {
    gradio: e,
    _internal: a,
    ...t
  } = s;
  return Object.keys(a).reduce((l, u) => {
    const r = u.match(/bind_(.+)_event/);
    if (r) {
      const i = r[1], n = i.split("_"), f = (...m) => {
        const b = m.map((o) => m && typeof o == "object" && (o.nativeEvent || o instanceof Event) ? {
          type: o.type,
          detail: o.detail,
          timestamp: o.timeStamp,
          clientX: o.clientX,
          clientY: o.clientY,
          targetId: o.target.id,
          targetClassName: o.target.className,
          altKey: o.altKey,
          ctrlKey: o.ctrlKey,
          shiftKey: o.shiftKey,
          metaKey: o.metaKey
        } : o);
        return e.dispatch(i.replace(/[A-Z]/g, (o) => "_" + o.toLowerCase()), {
          payload: b,
          component: t
        });
      };
      if (n.length > 1) {
        let m = {
          ...t.props[n[0]] || {}
        };
        l[n[0]] = m;
        for (let o = 1; o < n.length - 1; o++) {
          const g = {
            ...t.props[n[o]] || {}
          };
          m[n[o]] = g, m = g;
        }
        const b = n[n.length - 1];
        return m[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = f, l;
      }
      const h = n[0];
      l[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = f;
    }
    return l;
  }, {});
}
const {
  SvelteComponent: z,
  add_flush_callback: E,
  assign: p,
  bind: P,
  binding_callbacks: j,
  create_component: I,
  create_slot: N,
  destroy_component: A,
  detach: S,
  empty: U,
  exclude_internal_props: y,
  flush: d,
  get_all_dirty_from_scope: X,
  get_slot_changes: Y,
  get_spread_object: q,
  get_spread_update: L,
  handle_promise: O,
  init: Z,
  insert: w,
  mount_component: B,
  noop: _,
  safe_not_equal: D,
  transition_in: v,
  transition_out: k,
  update_await_block_branch: F,
  update_slot_base: G
} = window.__gradio__svelte__internal;
function H(s) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function J(s) {
  let e, a, t;
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
  function u(i) {
    s[11](i);
  }
  let r = {
    $$slots: {
      default: [M]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let i = 0; i < l.length; i += 1)
    r = p(r, l[i]);
  return (
    /*value*/
    s[0] !== void 0 && (r.value = /*value*/
    s[0]), e = new /*Expandable*/
    s[13]({
      props: r
    }), j.push(() => P(e, "value", u)), {
      c() {
        I(e.$$.fragment);
      },
      m(i, n) {
        B(e, i, n), t = !0;
      },
      p(i, n) {
        const f = n & /*$$props, gradio, props, as_item, visible, elem_id, elem_classes, elem_style*/
        766 ? L(l, [n & /*$$props*/
        512 && q(
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
        }), !a && n & /*value*/
        1 && (a = !0, f.value = /*value*/
        i[0], E(() => a = !1)), e.$set(f);
      },
      i(i) {
        t || (v(e.$$.fragment, i), t = !0);
      },
      o(i) {
        k(e.$$.fragment, i), t = !1;
      },
      d(i) {
        A(e, i);
      }
    }
  );
}
function M(s) {
  let e;
  const a = (
    /*#slots*/
    s[10].default
  ), t = N(
    a,
    s,
    /*$$scope*/
    s[12],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(l, u) {
      t && t.m(l, u), e = !0;
    },
    p(l, u) {
      t && t.p && (!e || u & /*$$scope*/
      4096) && G(
        t,
        a,
        l,
        /*$$scope*/
        l[12],
        e ? Y(
          a,
          /*$$scope*/
          l[12],
          u,
          null
        ) : X(
          /*$$scope*/
          l[12]
        ),
        null
      );
    },
    i(l) {
      e || (v(t, l), e = !0);
    },
    o(l) {
      k(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function Q(s) {
  return {
    c: _,
    m: _,
    p: _,
    i: _,
    o: _,
    d: _
  };
}
function R(s) {
  let e, a, t = {
    ctx: s,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Q,
    then: J,
    catch: H,
    value: 13,
    blocks: [, , ,]
  };
  return O(
    /*AwaitedExpandable*/
    s[8],
    t
  ), {
    c() {
      e = U(), t.block.c();
    },
    m(l, u) {
      w(l, e, u), t.block.m(l, t.anchor = u), t.mount = () => e.parentNode, t.anchor = e, a = !0;
    },
    p(l, [u]) {
      s = l, F(t, s, u);
    },
    i(l) {
      a || (v(t.block), a = !0);
    },
    o(l) {
      for (let u = 0; u < 3; u += 1) {
        const r = t.blocks[u];
        k(r);
      }
      a = !1;
    },
    d(l) {
      l && S(e), t.block.d(l), t.token = null, t = null;
    }
  };
}
function T(s, e, a) {
  let {
    $$slots: t = {},
    $$scope: l
  } = e;
  const u = C(() => import("./Expandable-CO9MUVZ8.js"));
  let {
    gradio: r
  } = e, {
    props: i = {}
  } = e, {
    value: n
  } = e, {
    as_item: f
  } = e, {
    visible: h = !0
  } = e, {
    elem_id: m = ""
  } = e, {
    elem_classes: b = []
  } = e, {
    elem_style: o = {}
  } = e;
  function g(c) {
    n = c, a(0, n);
  }
  return s.$$set = (c) => {
    a(9, e = p(p({}, e), y(c))), "gradio" in c && a(1, r = c.gradio), "props" in c && a(2, i = c.props), "value" in c && a(0, n = c.value), "as_item" in c && a(3, f = c.as_item), "visible" in c && a(4, h = c.visible), "elem_id" in c && a(5, m = c.elem_id), "elem_classes" in c && a(6, b = c.elem_classes), "elem_style" in c && a(7, o = c.elem_style), "$$scope" in c && a(12, l = c.$$scope);
  }, e = y(e), [n, r, i, f, h, m, b, o, u, e, t, g, l];
}
class W extends z {
  constructor(e) {
    super(), Z(this, e, T, R, D, {
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
