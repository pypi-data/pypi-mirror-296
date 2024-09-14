async function v() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((s) => {
    window.ms_globals.initialize = () => {
      s();
    };
  })), await window.ms_globals.initializePromise;
}
async function K(s) {
  return await v(), s().then((e) => e.default);
}
function M(s) {
  const {
    gradio: e,
    _internal: n,
    ...l
  } = s;
  return Object.keys(n).reduce((i, t) => {
    const a = t.match(/bind_(.+)_event/);
    if (a) {
      const _ = a[1], r = _.split("_"), b = (...u) => {
        const d = u.map((o) => u && typeof o == "object" && (o.nativeEvent || o instanceof Event) ? {
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
        return e.dispatch(_.replace(/[A-Z]/g, (o) => "_" + o.toLowerCase()), {
          payload: d,
          component: l
        });
      };
      if (r.length > 1) {
        let u = {
          ...l.props[r[0]] || {}
        };
        i[r[0]] = u;
        for (let o = 1; o < r.length - 1; o++) {
          const c = {
            ...l.props[r[o]] || {}
          };
          u[r[o]] = c, u = c;
        }
        const d = r[r.length - 1];
        return u[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = b, i;
      }
      const h = r[0];
      i[`on${h.slice(0, 1).toUpperCase()}${h.slice(1)}`] = b;
    }
    return i;
  }, {});
}
const {
  SvelteComponent: C,
  assign: g,
  create_component: z,
  create_slot: I,
  destroy_component: P,
  detach: j,
  empty: E,
  exclude_internal_props: y,
  flush: f,
  get_all_dirty_from_scope: N,
  get_slot_changes: A,
  get_spread_object: S,
  get_spread_update: U,
  handle_promise: X,
  init: Y,
  insert: q,
  mount_component: B,
  noop: m,
  safe_not_equal: L,
  transition_in: p,
  transition_out: k,
  update_await_block_branch: O,
  update_slot_base: Z
} = window.__gradio__svelte__internal;
function w(s) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function D(s) {
  let e, n;
  const l = [
    /*$$props*/
    s[9],
    {
      gradio: (
        /*gradio*/
        s[0]
      )
    },
    {
      props: (
        /*props*/
        s[1]
      )
    },
    {
      as_item: (
        /*as_item*/
        s[3]
      )
    },
    {
      title: (
        /*title*/
        s[2]
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
  let i = {
    $$slots: {
      default: [F]
    },
    $$scope: {
      ctx: s
    }
  };
  for (let t = 0; t < l.length; t += 1)
    i = g(i, l[t]);
  return e = new /*BreadcrumbItem*/
  s[12]({
    props: i
  }), {
    c() {
      z(e.$$.fragment);
    },
    m(t, a) {
      B(e, t, a), n = !0;
    },
    p(t, a) {
      const _ = a & /*$$props, gradio, props, as_item, title, visible, elem_id, elem_classes, elem_style*/
      767 ? U(l, [a & /*$$props*/
      512 && S(
        /*$$props*/
        t[9]
      ), a & /*gradio*/
      1 && {
        gradio: (
          /*gradio*/
          t[0]
        )
      }, a & /*props*/
      2 && {
        props: (
          /*props*/
          t[1]
        )
      }, a & /*as_item*/
      8 && {
        as_item: (
          /*as_item*/
          t[3]
        )
      }, a & /*title*/
      4 && {
        title: (
          /*title*/
          t[2]
        )
      }, a & /*visible*/
      16 && {
        visible: (
          /*visible*/
          t[4]
        )
      }, a & /*elem_id*/
      32 && {
        elem_id: (
          /*elem_id*/
          t[5]
        )
      }, a & /*elem_classes*/
      64 && {
        elem_classes: (
          /*elem_classes*/
          t[6]
        )
      }, a & /*elem_style*/
      128 && {
        elem_style: (
          /*elem_style*/
          t[7]
        )
      }]) : {};
      a & /*$$scope*/
      2048 && (_.$$scope = {
        dirty: a,
        ctx: t
      }), e.$set(_);
    },
    i(t) {
      n || (p(e.$$.fragment, t), n = !0);
    },
    o(t) {
      k(e.$$.fragment, t), n = !1;
    },
    d(t) {
      P(e, t);
    }
  };
}
function F(s) {
  let e;
  const n = (
    /*#slots*/
    s[10].default
  ), l = I(
    n,
    s,
    /*$$scope*/
    s[11],
    null
  );
  return {
    c() {
      l && l.c();
    },
    m(i, t) {
      l && l.m(i, t), e = !0;
    },
    p(i, t) {
      l && l.p && (!e || t & /*$$scope*/
      2048) && Z(
        l,
        n,
        i,
        /*$$scope*/
        i[11],
        e ? A(
          n,
          /*$$scope*/
          i[11],
          t,
          null
        ) : N(
          /*$$scope*/
          i[11]
        ),
        null
      );
    },
    i(i) {
      e || (p(l, i), e = !0);
    },
    o(i) {
      k(l, i), e = !1;
    },
    d(i) {
      l && l.d(i);
    }
  };
}
function G(s) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function H(s) {
  let e, n, l = {
    ctx: s,
    current: null,
    token: null,
    hasCatch: !1,
    pending: G,
    then: D,
    catch: w,
    value: 12,
    blocks: [, , ,]
  };
  return X(
    /*AwaitedBreadcrumbItem*/
    s[8],
    l
  ), {
    c() {
      e = E(), l.block.c();
    },
    m(i, t) {
      q(i, e, t), l.block.m(i, l.anchor = t), l.mount = () => e.parentNode, l.anchor = e, n = !0;
    },
    p(i, [t]) {
      s = i, O(l, s, t);
    },
    i(i) {
      n || (p(l.block), n = !0);
    },
    o(i) {
      for (let t = 0; t < 3; t += 1) {
        const a = l.blocks[t];
        k(a);
      }
      n = !1;
    },
    d(i) {
      i && j(e), l.block.d(i), l.token = null, l = null;
    }
  };
}
function J(s, e, n) {
  let {
    $$slots: l = {},
    $$scope: i
  } = e;
  const t = K(() => import("./BreadcrumbItem-tOg94-eB.js"));
  let {
    gradio: a
  } = e, {
    props: _ = {}
  } = e, {
    title: r = ""
  } = e, {
    as_item: b
  } = e, {
    visible: h = !0
  } = e, {
    elem_id: u = ""
  } = e, {
    elem_classes: d = []
  } = e, {
    elem_style: o = {}
  } = e;
  return s.$$set = (c) => {
    n(9, e = g(g({}, e), y(c))), "gradio" in c && n(0, a = c.gradio), "props" in c && n(1, _ = c.props), "title" in c && n(2, r = c.title), "as_item" in c && n(3, b = c.as_item), "visible" in c && n(4, h = c.visible), "elem_id" in c && n(5, u = c.elem_id), "elem_classes" in c && n(6, d = c.elem_classes), "elem_style" in c && n(7, o = c.elem_style), "$$scope" in c && n(11, i = c.$$scope);
  }, e = y(e), [a, _, r, b, h, u, d, o, t, e, l, i];
}
class Q extends C {
  constructor(e) {
    super(), Y(this, e, J, H, L, {
      gradio: 0,
      props: 1,
      title: 2,
      as_item: 3,
      visible: 4,
      elem_id: 5,
      elem_classes: 6,
      elem_style: 7
    });
  }
  get gradio() {
    return this.$$.ctx[0];
  }
  set gradio(e) {
    this.$$set({
      gradio: e
    }), f();
  }
  get props() {
    return this.$$.ctx[1];
  }
  set props(e) {
    this.$$set({
      props: e
    }), f();
  }
  get title() {
    return this.$$.ctx[2];
  }
  set title(e) {
    this.$$set({
      title: e
    }), f();
  }
  get as_item() {
    return this.$$.ctx[3];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), f();
  }
  get visible() {
    return this.$$.ctx[4];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), f();
  }
  get elem_id() {
    return this.$$.ctx[5];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), f();
  }
  get elem_classes() {
    return this.$$.ctx[6];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), f();
  }
  get elem_style() {
    return this.$$.ctx[7];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), f();
  }
}
export {
  Q as I,
  M as b
};
