import { g as U, w as d } from "./Index-Im5V1kMA.js";
const k = window.ms_globals.ReactDOM.createPortal, W = window.ms_globals.antd.Skeleton, {
  SvelteComponent: j,
  assign: v,
  binding_callbacks: y,
  check_outros: A,
  component_subscribe: S,
  compute_slots: B,
  create_slot: F,
  detach: f,
  element: K,
  empty: G,
  exclude_internal_props: h,
  get_all_dirty_from_scope: H,
  get_slot_changes: J,
  group_outros: L,
  init: Q,
  insert: m,
  safe_not_equal: T,
  set_custom_element_data: N,
  space: V,
  transition_in: p,
  transition_out: b,
  update_slot_base: X
} = window.__gradio__svelte__internal, {
  beforeUpdate: Y,
  getContext: Z,
  onDestroy: $,
  setContext: ee
} = window.__gradio__svelte__internal;
function C(l) {
  let t, n;
  const a = (
    /*#slots*/
    l[7].default
  ), s = F(
    a,
    l,
    /*$$scope*/
    l[6],
    null
  );
  return {
    c() {
      t = K("svelte-slot"), s && s.c(), N(t, "class", "svelte-1rt0kpf");
    },
    m(e, o) {
      m(e, t, o), s && s.m(t, null), l[9](t), n = !0;
    },
    p(e, o) {
      s && s.p && (!n || o & /*$$scope*/
      64) && X(
        s,
        a,
        e,
        /*$$scope*/
        e[6],
        n ? J(
          a,
          /*$$scope*/
          e[6],
          o,
          null
        ) : H(
          /*$$scope*/
          e[6]
        ),
        null
      );
    },
    i(e) {
      n || (p(s, e), n = !0);
    },
    o(e) {
      b(s, e), n = !1;
    },
    d(e) {
      e && f(t), s && s.d(e), l[9](null);
    }
  };
}
function te(l) {
  let t, n, a, s, e = (
    /*$$slots*/
    l[4].default && C(l)
  );
  return {
    c() {
      t = K("react-portal-target"), n = V(), e && e.c(), a = G(), N(t, "class", "svelte-1rt0kpf");
    },
    m(o, c) {
      m(o, t, c), l[8](t), m(o, n, c), e && e.m(o, c), m(o, a, c), s = !0;
    },
    p(o, [c]) {
      /*$$slots*/
      o[4].default ? e ? (e.p(o, c), c & /*$$slots*/
      16 && p(e, 1)) : (e = C(o), e.c(), p(e, 1), e.m(a.parentNode, a)) : e && (L(), b(e, 1, 1, () => {
        e = null;
      }), A());
    },
    i(o) {
      s || (p(e), s = !0);
    },
    o(o) {
      b(e), s = !1;
    },
    d(o) {
      o && (f(t), f(n), f(a)), l[8](null), e && e.d(o);
    }
  };
}
function P(l) {
  const {
    svelteInit: t,
    ...n
  } = l;
  return n;
}
function se(l, t, n) {
  let a, s, {
    $$slots: e = {},
    $$scope: o
  } = t;
  const c = B(e);
  let {
    svelteInit: i
  } = t;
  const w = d(P(t)), u = d();
  S(l, u, (r) => n(0, a = r));
  const _ = d();
  S(l, _, (r) => n(1, s = r));
  const I = [], x = Z("$$ms-gr-antd-react-wrapper"), {
    slotKey: R,
    slotIndex: q,
    subSlotIndex: z
  } = U() || {}, E = i({
    parent: x,
    props: w,
    target: u,
    slot: _,
    slotKey: R,
    slotIndex: q,
    subSlotIndex: z,
    onDestroy(r) {
      I.push(r);
    }
  });
  ee("$$ms-gr-antd-react-wrapper", E), Y(() => {
    w.set(P(t));
  }), $(() => {
    I.forEach((r) => r());
  });
  function M(r) {
    y[r ? "unshift" : "push"](() => {
      a = r, u.set(a);
    });
  }
  function O(r) {
    y[r ? "unshift" : "push"](() => {
      s = r, _.set(s);
    });
  }
  return l.$$set = (r) => {
    n(17, t = v(v({}, t), h(r))), "svelteInit" in r && n(5, i = r.svelteInit), "$$scope" in r && n(6, o = r.$$scope);
  }, t = h(t), [a, s, u, _, c, i, o, e, M, O];
}
class oe extends j {
  constructor(t) {
    super(), Q(this, t, se, te, T, {
      svelteInit: 5
    });
  }
}
const D = window.ms_globals.rerender, g = window.ms_globals.tree;
function ne(l) {
  function t(n) {
    const a = d(), s = new oe({
      ...n,
      props: {
        svelteInit(e) {
          window.ms_globals.autokey += 1;
          const o = {
            key: window.ms_globals.autokey,
            svelteInstance: a,
            reactComponent: l,
            props: e.props,
            slot: e.slot,
            target: e.target,
            slotIndex: e.slotIndex,
            subSlotIndex: e.subSlotIndex,
            slotKey: e.slotKey,
            nodes: []
          }, c = e.parent ?? g;
          return c.nodes = [...c.nodes, o], D({
            createPortal: k,
            node: g
          }), e.onDestroy(() => {
            c.nodes = c.nodes.filter((i) => i.svelteInstance !== a), D({
              createPortal: k,
              node: g
            });
          }), o;
        },
        ...n.props
      }
    });
    return a.set(s), s;
  }
  return new Promise((n) => {
    window.ms_globals.initializePromise.then(() => {
      n(t);
    });
  });
}
const re = ne(W.Node);
export {
  re as SkeletonNode,
  re as default
};
