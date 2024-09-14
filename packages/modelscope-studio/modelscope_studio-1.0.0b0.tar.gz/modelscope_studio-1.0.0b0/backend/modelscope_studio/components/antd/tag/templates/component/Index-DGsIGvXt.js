async function Z() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((n) => {
    window.ms_globals.initialize = () => {
      n();
    };
  })), await window.ms_globals.initializePromise;
}
async function B(n) {
  return await Z(), n().then((e) => e.default);
}
function R(n) {
  const {
    gradio: e,
    _internal: i,
    ...t
  } = n;
  return Object.keys(i).reduce((o, s) => {
    const l = s.match(/bind_(.+)_event/);
    if (l) {
      const u = l[1], r = u.split("_"), c = (...d) => {
        const b = d.map((_) => d && typeof _ == "object" && (_.nativeEvent || _ instanceof Event) ? {
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
        return e.dispatch(u.replace(/[A-Z]/g, (_) => "_" + _.toLowerCase()), {
          payload: b,
          component: t
        });
      };
      if (r.length > 1) {
        let d = {
          ...t.props[r[0]] || {}
        };
        o[r[0]] = d;
        for (let _ = 1; _ < r.length - 1; _++) {
          const g = {
            ...t.props[r[_]] || {}
          };
          d[r[_]] = g, d = g;
        }
        const b = r[r.length - 1];
        return d[`on${b.slice(0, 1).toUpperCase()}${b.slice(1)}`] = c, o;
      }
      const m = r[0];
      o[`on${m.slice(0, 1).toUpperCase()}${m.slice(1)}`] = c;
    }
    return o;
  }, {});
}
function N() {
}
function G(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
function H(n, ...e) {
  if (n == null) {
    for (const t of e)
      t(void 0);
    return N;
  }
  const i = n.subscribe(...e);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function w(n) {
  let e;
  return H(n, (i) => e = i)(), e;
}
const v = [];
function y(n, e = N) {
  let i;
  const t = /* @__PURE__ */ new Set();
  function o(u) {
    if (G(n, u) && (n = u, i)) {
      const r = !v.length;
      for (const c of t)
        c[1](), v.push(c, n);
      if (r) {
        for (let c = 0; c < v.length; c += 2)
          v[c][0](v[c + 1]);
        v.length = 0;
      }
    }
  }
  function s(u) {
    o(u(n));
  }
  function l(u, r = N) {
    const c = [u, r];
    return t.add(c), t.size === 1 && (i = e(o, s) || N), u(n), () => {
      t.delete(c), t.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: s,
    subscribe: l
  };
}
const {
  getContext: I,
  setContext: E
} = window.__gradio__svelte__internal, J = "$$ms-gr-antd-slots-key";
function Q() {
  const n = y({});
  return E(J, n);
}
const W = "$$ms-gr-antd-context-key";
function $(n) {
  var u;
  if (!Reflect.has(n, "as_item") || !Reflect.has(n, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const e = te(), i = ne({
    slot: void 0,
    index: n._internal.index,
    subIndex: n._internal.subIndex
  });
  e && e.subscribe((r) => {
    i.slotKey.set(r);
  }), ee();
  const t = I(W), o = ((u = w(t)) == null ? void 0 : u.as_item) || n.as_item, s = t ? o ? w(t)[o] : w(t) : {}, l = y({
    ...n,
    ...s
  });
  return t ? (t.subscribe((r) => {
    const {
      as_item: c
    } = w(l);
    c && (r = r[c]), l.update((m) => ({
      ...m,
      ...r
    }));
  }), [l, (r) => {
    const c = r.as_item ? w(t)[r.as_item] : w(t);
    return l.set({
      ...r,
      ...c
    });
  }]) : [l, (r) => {
    l.set(r);
  }];
}
const D = "$$ms-gr-antd-slot-key";
function ee() {
  E(D, y(void 0));
}
function te() {
  return I(D);
}
const F = "$$ms-gr-antd-component-slot-context-key";
function ne({
  slot: n,
  index: e,
  subIndex: i
}) {
  return E(F, {
    slotKey: y(n),
    slotIndex: y(e),
    subSlotIndex: y(i)
  });
}
function xe() {
  return I(F);
}
function se(n) {
  return n && n.__esModule && Object.prototype.hasOwnProperty.call(n, "default") ? n.default : n;
}
var L = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(n) {
  (function() {
    var e = {}.hasOwnProperty;
    function i() {
      for (var s = "", l = 0; l < arguments.length; l++) {
        var u = arguments[l];
        u && (s = o(s, t(u)));
      }
      return s;
    }
    function t(s) {
      if (typeof s == "string" || typeof s == "number")
        return s;
      if (typeof s != "object")
        return "";
      if (Array.isArray(s))
        return i.apply(null, s);
      if (s.toString !== Object.prototype.toString && !s.toString.toString().includes("[native code]"))
        return s.toString();
      var l = "";
      for (var u in s)
        e.call(s, u) && s[u] && (l = o(l, u));
      return l;
    }
    function o(s, l) {
      return l ? s ? s + " " + l : s + l : s;
    }
    n.exports ? (i.default = i, n.exports = i) : window.classNames = i;
  })();
})(L);
var ie = L.exports;
const U = /* @__PURE__ */ se(ie), {
  SvelteComponent: oe,
  assign: le,
  check_outros: M,
  component_subscribe: z,
  create_component: re,
  create_slot: ce,
  destroy_component: ue,
  detach: j,
  empty: O,
  flush: p,
  get_all_dirty_from_scope: ae,
  get_slot_changes: _e,
  get_spread_object: X,
  get_spread_update: fe,
  group_outros: T,
  handle_promise: me,
  init: de,
  insert: x,
  mount_component: be,
  noop: f,
  safe_not_equal: pe,
  set_data: he,
  text: ge,
  transition_in: h,
  transition_out: k,
  update_await_block_branch: ye,
  update_slot_base: ke
} = window.__gradio__svelte__internal;
function Y(n) {
  let e, i, t = {
    ctx: n,
    current: null,
    token: null,
    hasCatch: !1,
    pending: Pe,
    then: ve,
    catch: we,
    value: 19,
    blocks: [, , ,]
  };
  return me(
    /*AwaitedTag*/
    n[2],
    t
  ), {
    c() {
      e = O(), t.block.c();
    },
    m(o, s) {
      x(o, e, s), t.block.m(o, t.anchor = s), t.mount = () => e.parentNode, t.anchor = e, i = !0;
    },
    p(o, s) {
      n = o, ye(t, n, s);
    },
    i(o) {
      i || (h(t.block), i = !0);
    },
    o(o) {
      for (let s = 0; s < 3; s += 1) {
        const l = t.blocks[s];
        k(l);
      }
      i = !1;
    },
    d(o) {
      o && j(e), t.block.d(o), t.token = null, t = null;
    }
  };
}
function we(n) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function ve(n) {
  let e, i;
  const t = [
    {
      style: (
        /*$mergedProps*/
        n[0].elem_style
      )
    },
    {
      className: U(
        /*$mergedProps*/
        n[0].elem_classes,
        "ms-gr-antd-tag"
      )
    },
    {
      id: (
        /*$mergedProps*/
        n[0].elem_id
      )
    },
    /*$mergedProps*/
    n[0].props,
    R(
      /*$mergedProps*/
      n[0]
    ),
    {
      slots: (
        /*$slots*/
        n[1]
      )
    }
  ];
  let o = {
    $$slots: {
      default: [Se]
    },
    $$scope: {
      ctx: n
    }
  };
  for (let s = 0; s < t.length; s += 1)
    o = le(o, t[s]);
  return e = new /*Tag*/
  n[19]({
    props: o
  }), {
    c() {
      re(e.$$.fragment);
    },
    m(s, l) {
      be(e, s, l), i = !0;
    },
    p(s, l) {
      const u = l & /*$mergedProps, $slots*/
      3 ? fe(t, [l & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          s[0].elem_style
        )
      }, l & /*$mergedProps*/
      1 && {
        className: U(
          /*$mergedProps*/
          s[0].elem_classes,
          "ms-gr-antd-tag"
        )
      }, l & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          s[0].elem_id
        )
      }, l & /*$mergedProps*/
      1 && X(
        /*$mergedProps*/
        s[0].props
      ), l & /*$mergedProps*/
      1 && X(R(
        /*$mergedProps*/
        s[0]
      )), l & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          s[1]
        )
      }]) : {};
      l & /*$$scope, $mergedProps*/
      131073 && (u.$$scope = {
        dirty: l,
        ctx: s
      }), e.$set(u);
    },
    i(s) {
      i || (h(e.$$.fragment, s), i = !0);
    },
    o(s) {
      k(e.$$.fragment, s), i = !1;
    },
    d(s) {
      ue(e, s);
    }
  };
}
function Ce(n) {
  let e = (
    /*$mergedProps*/
    n[0].value + ""
  ), i;
  return {
    c() {
      i = ge(e);
    },
    m(t, o) {
      x(t, i, o);
    },
    p(t, o) {
      o & /*$mergedProps*/
      1 && e !== (e = /*$mergedProps*/
      t[0].value + "") && he(i, e);
    },
    i: f,
    o: f,
    d(t) {
      t && j(i);
    }
  };
}
function Ke(n) {
  let e;
  const i = (
    /*#slots*/
    n[16].default
  ), t = ce(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  return {
    c() {
      t && t.c();
    },
    m(o, s) {
      t && t.m(o, s), e = !0;
    },
    p(o, s) {
      t && t.p && (!e || s & /*$$scope*/
      131072) && ke(
        t,
        i,
        o,
        /*$$scope*/
        o[17],
        e ? _e(
          i,
          /*$$scope*/
          o[17],
          s,
          null
        ) : ae(
          /*$$scope*/
          o[17]
        ),
        null
      );
    },
    i(o) {
      e || (h(t, o), e = !0);
    },
    o(o) {
      k(t, o), e = !1;
    },
    d(o) {
      t && t.d(o);
    }
  };
}
function Se(n) {
  let e, i, t, o;
  const s = [Ke, Ce], l = [];
  function u(r, c) {
    return (
      /*$mergedProps*/
      r[0]._internal.layout ? 0 : 1
    );
  }
  return e = u(n), i = l[e] = s[e](n), {
    c() {
      i.c(), t = O();
    },
    m(r, c) {
      l[e].m(r, c), x(r, t, c), o = !0;
    },
    p(r, c) {
      let m = e;
      e = u(r), e === m ? l[e].p(r, c) : (T(), k(l[m], 1, 1, () => {
        l[m] = null;
      }), M(), i = l[e], i ? i.p(r, c) : (i = l[e] = s[e](r), i.c()), h(i, 1), i.m(t.parentNode, t));
    },
    i(r) {
      o || (h(i), o = !0);
    },
    o(r) {
      k(i), o = !1;
    },
    d(r) {
      r && j(t), l[e].d(r);
    }
  };
}
function Pe(n) {
  return {
    c: f,
    m: f,
    p: f,
    i: f,
    o: f,
    d: f
  };
}
function Ne(n) {
  let e, i, t = (
    /*$mergedProps*/
    n[0].visible && Y(n)
  );
  return {
    c() {
      t && t.c(), e = O();
    },
    m(o, s) {
      t && t.m(o, s), x(o, e, s), i = !0;
    },
    p(o, [s]) {
      /*$mergedProps*/
      o[0].visible ? t ? (t.p(o, s), s & /*$mergedProps*/
      1 && h(t, 1)) : (t = Y(o), t.c(), h(t, 1), t.m(e.parentNode, e)) : t && (T(), k(t, 1, 1, () => {
        t = null;
      }), M());
    },
    i(o) {
      i || (h(t), i = !0);
    },
    o(o) {
      k(t), i = !1;
    },
    d(o) {
      o && j(e), t && t.d(o);
    }
  };
}
function je(n, e, i) {
  let t, o, s, {
    $$slots: l = {},
    $$scope: u
  } = e;
  const r = B(() => import("./tag-HhZ9nc1b.js"));
  let {
    gradio: c
  } = e, {
    props: m = {}
  } = e;
  const d = y(m);
  z(n, d, (a) => i(15, t = a));
  let {
    _internal: b = {}
  } = e, {
    as_item: _
  } = e, {
    value: g = ""
  } = e, {
    visible: C = !0
  } = e, {
    elem_id: K = ""
  } = e, {
    elem_classes: S = []
  } = e, {
    elem_style: P = {}
  } = e;
  const [q, V] = $({
    gradio: c,
    props: t,
    _internal: b,
    visible: C,
    elem_id: K,
    elem_classes: S,
    elem_style: P,
    as_item: _,
    value: g
  });
  z(n, q, (a) => i(0, o = a));
  const A = Q();
  return z(n, A, (a) => i(1, s = a)), n.$$set = (a) => {
    "gradio" in a && i(6, c = a.gradio), "props" in a && i(7, m = a.props), "_internal" in a && i(8, b = a._internal), "as_item" in a && i(9, _ = a.as_item), "value" in a && i(10, g = a.value), "visible" in a && i(11, C = a.visible), "elem_id" in a && i(12, K = a.elem_id), "elem_classes" in a && i(13, S = a.elem_classes), "elem_style" in a && i(14, P = a.elem_style), "$$scope" in a && i(17, u = a.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty & /*props*/
    128 && d.update((a) => ({
      ...a,
      ...m
    })), n.$$.dirty & /*gradio, $updatedProps, _internal, visible, elem_id, elem_classes, elem_style, as_item, value*/
    65344 && V({
      gradio: c,
      props: t,
      _internal: b,
      visible: C,
      elem_id: K,
      elem_classes: S,
      elem_style: P,
      as_item: _,
      value: g
    });
  }, [o, s, r, d, q, A, c, m, b, _, g, C, K, S, P, t, l, u];
}
class ze extends oe {
  constructor(e) {
    super(), de(this, e, je, Ne, pe, {
      gradio: 6,
      props: 7,
      _internal: 8,
      as_item: 9,
      value: 10,
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
    }), p();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(e) {
    this.$$set({
      props: e
    }), p();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(e) {
    this.$$set({
      _internal: e
    }), p();
  }
  get as_item() {
    return this.$$.ctx[9];
  }
  set as_item(e) {
    this.$$set({
      as_item: e
    }), p();
  }
  get value() {
    return this.$$.ctx[10];
  }
  set value(e) {
    this.$$set({
      value: e
    }), p();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(e) {
    this.$$set({
      visible: e
    }), p();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(e) {
    this.$$set({
      elem_id: e
    }), p();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(e) {
    this.$$set({
      elem_classes: e
    }), p();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(e) {
    this.$$set({
      elem_style: e
    }), p();
  }
}
export {
  ze as I,
  xe as g,
  y as w
};
